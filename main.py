import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, run_tool
from Utilities.utilites import log


load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)
msg = []

MAX_STEPS = 10

msg.append(
    {
        "role":"system",
        "content":"Act like a very humble agent and respond always in under 20 words."
    }
)

while True:
    user_input = input("👦 You : ")
    if user_input == "exit":
        print("Exiting the program....")
        break

    msg.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=msg,
            tools =TOOLS
        )
        mssg = response.choices[0].message
        if not mssg.tool_calls:
            break
        log(f"Step {step+1}: model requested {len(mssg.tool_calls)} tool call(s)")
        msg.append(mssg)

        for tool_call in mssg.tool_calls:
            result = run_tool(tool_call)
            msg.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content": str(result)
            })
    else:
        #ran out of steps:  The model never gave the final answer
        fallback = "Sorry i could not finish this in with in steps limit."
        msg.append({
            "role" : "assistant",
            "content" : fallback
        })
        print("🤖 Assistant : " + fallback)
        continue
        
    msg.append({
        "role" : "assistant",
        "content" : mssg.content
    })

    print("🤖 Assistant : " + (mssg.content or "{}"))