from agent import run_agent, SYSTEM_PROMPT


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:

    question = input("\nAsk Your business question: ")

    if question.lower() in ["exit" "quit"]:
        print("Goodbye")
        break

    messages.append({
        "role": "user",
        "content": question
    })


    answer = run_agent(messages)

    print("\n==============================")
    print("FINAL AI ANSWER")
    print("==============================")
    print(answer)
    
