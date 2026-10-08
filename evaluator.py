from agent import run_agent, SYSTEM_PROMPT


TEST_CASES = [
    {
        "question": "Which country has the highest sales?",
        "expected": ["Mexico", "47217.30"]
    },
    {
        "question": "Which category has the highest sales?",
        "expected": ["Furniture", "256274.68"]
    },
    {
        "question": "Which product generates the highest total sales?",
        "expected": ["Standing Desk Converter", "46614.22"]
    },
    {
        "question": "Which customer segment generates the highest total profit?",
        "expected": ["Consumer", "87300.36"]
    },
    {
        "question": "Which country has the highest profit margin?",
        "expected": ["United States", "33.82"]
    }
]


def normalize(text):
    return text.lower().replace(",", "").replace("$", "").strip()


def evaluate_answer(answer, expected_values):

    answer = normalize(answer)

    for value in expected_values:
        value = normalize(value)

        if value not in answer:
            return False

    return True


def run_evaluation():

    passed = 0
    failed = 0

    print("\n==============================")
    print("AI DATA ANALYST EVALUATION")
    print("==============================")

    for index, test in enumerate(TEST_CASES, start=1):

        print(f"\nTest {index}")
        print(f"Question: {test['question']}")

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": test["question"]
            }
        ]

        answer = run_agent(messages)

        print("\nAI Answer:")
        print(answer)

        result = evaluate_answer(
            answer,
            test["expected"]
        )

        if result:
            print("Status: PASS")
            passed += 1

        else:
            print("Status: FAIL")
            failed += 1

    total = len(TEST_CASES)

    print("\n==============================")
    print("EVALUATION SUMMARY")
    print("==============================")

    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    accuracy = (passed / total) * 100

    print(f"Accuracy    : {accuracy:.2f}%")

    if accuracy == 100:
        print("\nAll tests passed successfully!")

    else:
        print("\nSome tests failed. Review the agent.")


if __name__ == "__main__":
    run_evaluation()