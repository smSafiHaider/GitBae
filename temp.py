import os
import google.generativeai as genai

from functions import get_repo_info, get_repo_contents, read_file_content
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = '''
                You are an helpful AI assistant that helps developers understand the contents of a GitHub repository. You will be provided with a link to a Github repositroy and some function calls. You have to use those function calls to fetch the contents of the repository as asked by the user, and give answer to the users question in detail.
                Only give the answer to what is asked, and be precise. Do not give the output in the form of Markdown or code. Also remember when explaining code also provide its references from the file. And Please remember that before printing answer please write "GITBAE: ".
'''

def start_chat_session():
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest",
                                  system_instruction=SYSTEM_PROMPT,
                                  tools=[get_repo_info, get_repo_contents, read_file_content])
    
    chat = model.start_chat(enable_automatic_function_calling=True, history=[])
    return chat



def main():

    chat = start_chat_session()
    while True:
        query = input("USER: ")
        if query == "exit":
            break
        response = chat.send_message(query)
        print(response.text)
    for content in chat.history:
        part = content.parts[0]
        print(content.role, "->", type(part).to_dict(part))
        print('-'*80)

if __name__ == "__main__":
    main()
