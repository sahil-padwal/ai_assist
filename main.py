from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)
msg = []

msg.append(
    {
        "role":"system",
        "content":"Act like a very humble agent and respond always in under 20 words."
    }
)

while True:
    user_input = input("You : ")
    if user_input == "exit":
        print("Exiting the program....")
        break

    msg.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=msg
    )
    print("Assist : " + response.choices[0].message.content)

    msg.append(
        {
            "role":"assistant",
            "content":response.choices[0].message.content
        }
    )
    