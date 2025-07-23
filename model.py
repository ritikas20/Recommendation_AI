import google.generativeai as genai
from config import os
from database import sql_query

system_prompt = """<your_system_prompt>"""  # reuse your system_prompt here

sql_gemini = None
chat = None

def init_model():
    global sql_gemini, chat
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))
    sql_gemini = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
        tools=[sql_query]
    )
    chat = sql_gemini.start_chat(enable_automatic_function_calling=True)
    return chat
