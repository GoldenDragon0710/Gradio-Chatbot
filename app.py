import gradio as gr
import openai
from loguru import logger
from typing import List
from pydantic import BaseModel
import markdown
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('API_KEY')

messages = [{"role": "assistant",
             "content": "Hello there! \n I'm Alfred Penny. \n At your service..."}]

css_styles = ""
with open("public/css/style.css", "r") as f:
    css_styles = f.read()


class Message(BaseModel):
    role: str
    content: str


def make_completion(messages: List[Message]):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    except:
        print("--------create error------")


def page_refresh():
    onclick = "location.reload();"
    refresh_btn = "<div class='refresh_btn' onclick='{}'>".format(onclick)
    refresh_btn += "<img src='file/public/img/refresh.svg'/>"
    refresh_btn += "</div>"
    return refresh_btn


def predict(input):
    messages.append({"role": "user", "content": input})
    msg = [{"role": "system", "content": "Your name is Alfred Penny, you are a human"},
           {"role": "user", "content": input}]
    response = make_completion(msg)
#   response = res.replace("\n\n", "\n")
    messages.append({"role": "assistant", "content": response})
    return chatbot_container()


def chatbot_container():
    chat_history = "<div class='chat_content'>"
    onclick_like = "let modalElement=document.getElementById(\"feedback_modal\"); modalElement.style.display=\"block\"; let textareaElement = document.querySelector(\"#feedback_input_container textarea\"); textareaElement.setAttribute(\"placeholder\", \"What do you like about the response?\");"
    onclick_dislike = "let modalElement=document.getElementById(\"feedback_modal\"); modalElement.style.display=\"block\"; let textareaElement = document.querySelector(\"#feedback_input_container textarea\"); textareaElement.setAttribute(\"placeholder\", \"What do you dislike about the response?\");"
    for index, msg in enumerate(messages):
        if msg["role"] == "user":
            chat_history += "<div id='array_{}' class='chat_text {}'>{}</div>".format(
                index, msg["role"], markdown.markdown(msg["content"], output_format='html5'))
        elif msg["role"] == "assistant":
            chat_history += "<div id='array_{}' class='chat_text {}'>{}<div class='feedback_group'><div class='feedback_btns' onclick='{}'><img src='file/public/img/like.svg'/></div><div class='feedback_btns' onclick='{}'><img src='file/public/img/dislike.svg'/></div></div></div>".format(
                index, msg["role"], markdown.markdown(msg["content"], output_format='html5'), onclick_like, onclick_dislike)
    chat_history += "</div>"
    return chat_history


def msg_send_btn():
    onclick = "let modalElement=document.getElementById(\"input_record_btn\"); modalElement.style.display=\"none\"; let modalElement=document.getElementById(\"input_send_btn\"); modalElement.style.right=\"15px\";"
    msg_send_btn = "<div class='input_buttons' onclick='{}'>".format(onclick)
    msg_send_btn += "<img src='file/public/img/enter.svg'/>"
    msg_send_btn += "</div>"
    return msg_send_btn


def msg_record_btn():
    onclick = "let modalElement=document.getElementById(\"record_modal\"); modalElement.style.display=\"block\"; let contentElement=document.getElementById(\"chat_content\"); contentElement.style.height=\"calc(100vh - 60px - 170px)\";"
    msg_record_btn = "<div class='input_buttons' onclick='{}'>".format(onclick)
    msg_record_btn += "<img src='file/public/img/record.svg'/>"
    msg_record_btn += "</div>"
    return msg_record_btn


def modal_record_btn():
    print("Recording started...")


def record_modal_close_btn():
    onclick = "let modalElement = document.getElementById(\"record_modal\"); modalElement.style.display=\"none\"; let contentElement=document.getElementById(\"chat_content\"); contentElement.style.height=\"calc(100vh - 60px - 110px)\";"
    close_button = "<div class='close_button' onclick='{}'>".format(onclick)
    close_button += "<img src='file/public/img/close.svg'/>"
    close_button += "</div>"
    return close_button


def feedback_modal_close_btn():
    onclick = "let modalElement = document.getElementById(\"feedback_modal\"); modalElement.style.display=\"none\";"
    close_button = "<div class='close_button' onclick='{}'>".format(onclick)
    close_button += "<img src='file/public/img/close.svg'/>"
    close_button += "</div>"
    return close_button


def download_modal_close_btn():
    onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"none\";"
    close_button = "<div class='close_button' onclick='{}'>".format(onclick)
    close_button += "<img src='file/public/img/close.svg'/>"
    close_button += "</div>"
    return close_button


def limit_modal_close_btn():
    onclick = "let modalElement = document.getElementById(\"limit_modal\"); modalElement.style.display=\"none\";"
    close_button = "<div class='close_button' onclick='{}'>".format(onclick)
    close_button += "<img src='file/public/img/close.svg'/>"
    close_button += "</div>"
    return close_button


def download_submodal_show_btn():
    onclick = "let virtual_element = document.getElementById(\"virtual_element\");let state = virtual_element.querySelector(\"p\").innerHTML;let modalElement = document.getElementById(\"download_submodal\");let imgElement = document.querySelector(\".arrow_button img\");let arrowElement = document.getElementById(\"submodal_show_btn\");state == \"true\" ? (modalElement.style.display=\"block\", arrowElement.style.bottom=\"90px\", virtual_element.querySelector(\"p\").innerHTML=\"false\", imgElement.setAttribute(\"src\", \"file/public/img/down_arrow.svg\")) : (modalElement.style.display=\"none\",arrowElement.style.bottom=\"0\", virtual_element.querySelector(\"p\").innerHTML=\"true\", imgElement.setAttribute(\"src\", \"file/public/img/up_arrow.svg\"));"
    show_button = "<div class='arrow_button' onclick='{}'>".format(onclick)
    show_button += "<img src='file/public/img/up_arrow.svg'/>"
    show_button += "</div>"
    return show_button


def sendFeedback(input):
    print("feedback----", input)


def submitDownload(input):
    print("download----", input)


def AppStore():
    onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"block\";"
    appstore = "<div class='download_button_container' onclick='{}'>".format(
        onclick)
    appstore += "<img src='file/public/img/appstore.svg'/>"
    appstore += "<div class='download_button_text'><h5>Download on the</h5><h3>App Store</h3></div>"
    appstore += "</div>"
    return appstore


def GooglePlay():
    onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"block\";"
    google = "<div class='download_button_container' onclick='{}'>".format(
        onclick)
    google += "<img src='file/public/img/google.svg'/>"
    google += "<div class='download_button_text'><h5>GET IT ON</h5><h3>Google Play</h3></div>"
    google += "</div>"
    return google


def error_modal():
    error = "<div class='error_container'>"
    error += "<div class='error_icon'><img src='file/public/img/error.svg'/></div>"
    error += "<h1>Oops!</h1>"
    error += "<h3>Sorry, we're experiencing high traffic.</h3>"
    error += "<h3>Please try again later</h3>"
    error += "</div>"
    return error


with gr.Blocks(css=css_styles) as demo:
    logger.info("Starting Demo...")

    with gr.Row():
        header = gr.Markdown(
            value="""<center><img src="file/public/img/face.jpg" class="logo"/><img src="file/public/img/title.svg" class="logo_title"/></center>""", elem_id="header")
    gr.HTML(value=page_refresh, elem_id="page_refresh")
    chatbot = gr.HTML(value=chatbot_container, elem_id="chatbot_container")

    with gr.Row(elem_id="input_container"):
        txt = gr.Textbox(show_label=False, max_lines=2, placeholder="How do you feel today?",
                         elem_id="input_content").style(container=False)
        send_btn = gr.Button("", elem_id="input_send_btn")
        send_btn.click(fn=predict, inputs=[txt], outputs=[chatbot])
        gr.HTML(value=msg_record_btn, elem_id="input_record_btn")
        with gr.Row(elem_id="download_submodal"):
            gr.Markdown(
                value="""<h5><center>Download the app</center></h5>""", elem_id="footer")
            with gr.Row(elem_id="download_submodal_content"):
                gr.HTML(value=AppStore, elem_id="appstore")
                gr.HTML(value=GooglePlay, elem_id="googleplay")
    txt.submit(predict, inputs=[txt], outputs=[chatbot])
    chatbot1 = gr.HTML(visible=False)
    chatbot.change(lambda x: x, chatbot, chatbot1,
                   _js="(x) => document.getElementsByClassName('chat_content')[0].scrollTop = document.getElementsByClassName('chat_content')[0].scrollHeight")

    with gr.Row(elem_id="record_modal"):
        with gr.Row():
            listen_title = gr.Markdown(
                value="""<h2><center>Listening</center></h2>""", elem_id="listentitle")
        with gr.Row():
            recording = gr.Button("", elem_id="modal_record_btn")
            recording.click(fn=modal_record_btn)
        gr.HTML(value=record_modal_close_btn, elem_id="modal_close_btn")

    with gr.Row(elem_id="feedback_modal"):
        with gr.Row():
            listen_title = gr.Markdown(
                value="""<h3><center>Rating feedback</center></h3>""", elem_id="feedbacktitle")
        with gr.Row(elem_id="feedback_input_container"):
            with gr.Row():
                txt_feedback = gr.Textbox(
                    show_label=False, lines=3, placeholder="What do you dislike about the response?", elem_id="modal_input").style(container=False)
            send_feedback = gr.Button(value="Submit feedback")
            send_feedback.click(fn=sendFeedback, inputs=txt_feedback)
        gr.HTML(value=feedback_modal_close_btn, elem_id="modal_close_btn")

    with gr.Row(elem_id="download_modal"):
        with gr.Row():
            listen_title = gr.Markdown(
                value="""<h3><center>We're on it!</center></h3>""", elem_id="downloadtitle")
        with gr.Row(elem_id="download_input_container"):
            gr.Markdown(
                value="""<h3>Leave your email to get notified once the app is available in your country</h3>""", elem_id="download_label")
            with gr.Row():
                txt_download = gr.Textbox(
                    show_label=False, lines=1, placeholder="hi@email.com", elem_id="modal_input").style(container=False)
            submit_download = gr.Button(value="Submit")
            submit_download.click(fn=submitDownload, inputs=txt_download)
        gr.HTML(value=download_modal_close_btn, elem_id="modal_close_btn")

    with gr.Row(elem_id="limit_modal"):
        gr.HTML(value=error_modal, elem_id="error_modal_container")
        gr.HTML(value=limit_modal_close_btn, elem_id="modal_close_btn")

    with gr.Row(elem_id="submodal"):
        submodalbtn = gr.HTML(
            value=download_submodal_show_btn, elem_id="submodal_show_btn")
    # gr.HTML(value="<h3>Hello there!</h3>", elem_id="animation1")
    # gr.HTML(value="<h3>My name is Alfred Penny</h3>", elem_id="animation2")
    # gr.HTML(value="<h3>At your service...</h3>", elem_id="animation3")
    gr.HTML(value="<p>true</p>", elem_id="virtual_element")

demo.launch(server_port=8080)
