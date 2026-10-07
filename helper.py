import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads OPENAI_API_KEY from .env
client = OpenAI()
MODEL = "gpt-4o-mini"  # cheap and fast; swap in any current model

PROMPT = """You are a senior engineer helping debug CI failures.
Here's a failing CI or test log. Give me:
1. The most likely cause
2. The smallest fix
3. How to verify it
If you're not sure, say so. Don't invent details that aren't in the log.

Answer in uder 80, tight with exact commands.

LOG:
{log}"""

def main():
    if len(sys.argv) > 1:
        log = open(sys.argv[1]).read()
    else:
        log = sys.stdin.read()
    log = log[-8000:]  # keep the tail, where errors usually are

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT.format(log=log)}],
        temperature=0,
    )
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    main()