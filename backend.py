#this file contains all the backend logic of the agent basically the tools will be used here
from groq import Groq
from dotenv import  load_dotenv
import os
load_dotenv()
system=os.getenv("System_identity")
client = Groq(api_key=os.getenv("GROQ_API_KEY"),)
def get_response(prompt):
 try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response=""
    for chunk in completion:
        content=chunk.choices[0].delta.content or ""
        yield content
    return response
 except Exception as e:
     print(f"an error has occured{e}")
     yield f"Error:{e}"
     
     
    