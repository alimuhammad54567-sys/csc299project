from openai import OpenAI

client = OpenAI()

# List of paragraph-length task descriptions
task_descriptions = [
    "Develop a mobile application that allows users to track their daily water intake and sends reminders throughout the day. The app should include data visualization and goal-setting features.",
    "Write a research paper analyzing how artificial intelligence impacts the job market, focusing on automation, new opportunities, and skill shifts in the workforce."
]

print("🧠 Task Summarizer\n")

for i, desc in enumerate(task_descriptions, start=1):
    print(f"Task {i}:")
    print(desc)
    print("\nSummary:")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a concise assistant that summarizes tasks into short phrases."},
            {"role": "user", "content": desc}
        ]
    )

    summary = response.choices[0].message.content.strip()
    print(summary)
    print("\n" + "-" * 60 + "\n")
