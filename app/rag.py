from app.retrieval import search_documents, extract_cpt_code
from app.reranker import rerank_documents
from app.guardrails import get_guardrails
from app.prompts import RAG_PROMPT
from app.cache import get_cached_answer, set_cached_answer


def build_context(documents):
    context_parts = []

    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page_number", "Unknown")

        context_parts.append(
            f"""
Source {index}
Document: {source}
Page: {page}

Content:
{document.page_content}
"""
        )

    return "\n".join(context_parts)


def ask_question(question: str):

    # ---------------------------------------------------------
    # 1. Check Redis cache
    # ---------------------------------------------------------
    cached_result = get_cached_answer(question)

    if cached_result:
        print("Redis cache HIT")
        return cached_result

    print("Redis cache MISS")

    # ---------------------------------------------------------
    # 2. Retrieve documents from Qdrant
    # ---------------------------------------------------------
    results = search_documents(
        query=question,
        k=10,
    )

    documents = [document for document, score in results]

    if not documents:
        result = {
            "answer": "No relevant information was found.",
            "sources": [],
        }

        set_cached_answer(question, result)
        return result

    # ---------------------------------------------------------
    # 3. CPT-aware reranking
    # ---------------------------------------------------------
    cpt_code = extract_cpt_code(question)

    if cpt_code:
        rerank_query = cpt_code
    else:
        rerank_query = question

    reranked_documents = rerank_documents(
        query=rerank_query,
        documents=documents,
        top_k=3,
    )

    # ---------------------------------------------------------
    # 4. Build RAG context
    # ---------------------------------------------------------
    context = build_context(reranked_documents)

    formatted_prompt = RAG_PROMPT.format(
        context=context,
        question=question,
    )

    # ---------------------------------------------------------
    # 5. NeMo Guardrails + Gemini
    # ---------------------------------------------------------
    rails = get_guardrails()

    response = rails.generate(
        messages=[
            {
                "role": "system",
                "content": formatted_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )

    answer = response["content"]

    # ---------------------------------------------------------
    # 6. Prepare sources
    # ---------------------------------------------------------
    sources = []

    for document in reranked_documents:
        sources.append(
            {
                "source": document.metadata.get("source"),
                "page": document.metadata.get("page_number"),
                "score": document.metadata.get("rerank_score"),
            }
        )

    result = {
        "answer": answer,
        "sources": sources,
    }

    # ---------------------------------------------------------
    # 7. Store result in Redis
    # ---------------------------------------------------------
    set_cached_answer(
        question=question,
        result=result,
        ttl=3600,
    )

    return result