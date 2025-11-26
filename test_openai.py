import os, openai
print("OPENAI_API_KEY present:", bool(os.environ.get("OPENAI_API_KEY")))
openai.api_key = os.environ.get("OPENAI_API_KEY")
try:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":"Hello"}],
        max_tokens=10
    )
    print("Success:", resp.choices[0].message.content.strip())
except Exception as e:
    print("ERROR:", type(e).__name__, e)
