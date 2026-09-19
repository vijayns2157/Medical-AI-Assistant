from app.guardrails import get_guardrails


def main():
    print("=" * 60)
    print("NEMO GUARDRAILS TEST")
    print("=" * 60)

    rails = get_guardrails()

    response = rails.generate(
        messages=[
            {
                "role": "user",
                "content": (
                    "What is the place of service "
                    "code for telehealth?"
                ),
            }
        ]
    )

    print("\nResponse:")
    print(response)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()