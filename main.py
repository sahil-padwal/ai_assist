from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json
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
        messages=msg,
        tools =TOOLS
    )
    mssg = response.choices[0].message
    if mssg.tool_calls:
        msg.append(mssg)

        for tool_call in mssg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)
            msg.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content": str(result)
            })

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=msg,
            tools=TOOLS
        )
        mssg = response.choices[0].message
    msg.append({
        "role" : "assistant",
        "content" : mssg.content
    })

    print("Assistant : " + (mssg.content or "{}"))