from openai import OpenAI

def summarize_task(client, description: str) -> str:
    """Send a paragraph-length description to ChatGPT and return a short summary phrase."""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes tasks concisely."},
            {"role": "user", "content": f"Summarize this task in 5 words or fewer:\n\n{description}"}
        ],
    )
    return response.choices[0].message.content.strip()

def main():
    client = OpenAI()

    # Sample paragraph-length task descriptions
    tasks = [
        """Develop a Python-based terminal app that helps users track national parks they've visited.
        Include features for marking parks as visited, adding notes, viewing maps, and chatting with an AI assistant.""",

        """Create a web app prototype that visualizes environmental data across U.S. states,
        with charts for pollution, population, and climate, allowing users to explore trends interactively."""
    ]

    print("🧠 Task Summarizer (ChatGPT-5-mini)\n")

    for i, task in enumerate(tasks, start=1):
        summary = summarize_task(client, task)
        print(f"Task {i} Summary: {summary}")

if __name__ == "__main__":
    main()
