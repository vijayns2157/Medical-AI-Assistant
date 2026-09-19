from pathlib import Path

from nemoguardrails import LLMRails, RailsConfig

from app.llm import get_llm


GUARDRAILS_PATH = Path("guardrails")


def get_guardrails():
    config = RailsConfig.from_path(
        str(GUARDRAILS_PATH)
    )

    llm = get_llm()

    rails = LLMRails(
        config,
        llm=llm,
    )

    return rails