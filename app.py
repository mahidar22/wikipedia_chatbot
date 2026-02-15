import os
import gradio as gr
import wikipedia
import wikipediaapi
from transformers import pipeline

# Load lighter QA model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad"
)

wiki_api = wikipediaapi.Wikipedia(
    user_agent="WikiChatbot/1.0 (mahidarreddyilluri@gmail.com)",
    language="en"
)

current_context = ""

def search_and_load(topic):
    global current_context

    search_results = wikipedia.search(topic)
    if not search_results:
        return "No matching Wikipedia page found."

    page_title = search_results[0]
    page = wiki_api.page(page_title)

    if not page.exists():
        return "Page not found."

    current_context = page.text[:4000]
    return f"Loaded topic: {page_title}. Now ask your question."

def chatbot(message, history):
    global current_context

    try:
        # If no topic loaded → treat first message as topic
        if current_context == "":
            return search_and_load(message)

        result = qa_pipeline(
            question=message,
            context=current_context
        )

        answer = result.get("answer", "")

        if answer.strip() == "":
            answer = "I could not find a clear answer."

        return answer

    except Exception as e:
        return f"Error: {str(e)}"

def reset_chat():
    global current_context
    current_context = ""
    return []

with gr.Blocks() as demo:
    gr.Markdown("# Wikipedia Smart Chatbot")

    chatbot_ui = gr.ChatInterface(
        fn=chatbot
    )

    reset_button = gr.Button("Reset Topic")
    reset_button.click(reset_chat, outputs=chatbot_ui)

demo.launch()
port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)