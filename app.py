import gradio as gr
import wikipedia
import os

current_topic = ""

def chatbot(message, history):
    global current_topic

    try:
        # First message = topic
        if current_topic == "":
            search_results = wikipedia.search(message)
            if not search_results:
                return "No matching topic found."

            current_topic = search_results[0]
            return f"Loaded topic: {current_topic}. Ask your question."

        # Answer using summary
        summary = wikipedia.summary(current_topic, sentences=5)
        return summary

    except Exception as e:
        return f"Error: {str(e)}"

def reset_chat():
    global current_topic
    current_topic = ""
    return []

with gr.Blocks() as demo:
    gr.Markdown("# Wikipedia Chatbot (Lightweight Version)")

    chat = gr.ChatInterface(fn=chatbot)

    reset_button = gr.Button("Reset Topic")
    reset_button.click(reset_chat, outputs=chat)

port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)
