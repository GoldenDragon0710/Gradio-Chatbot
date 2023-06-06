import gradio as gr
import openai
from loguru import logger
from typing import List
from pydantic import BaseModel
import markdown
# import pyaudio
# import wave
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('API_KEY')
# audio = pyaudio.PyAudio()
# stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

messages = [{"role": "assistant", "content": "Hello there! \n I'm Alfred Penny. \n At your service..."}]

css="""
.gradio-container {
  background-color: #28351b;
  padding:unset !important;
  max-width:900px !important;
}
gradio-app {
  background-color: #28351b !important;
}
footer {
  display: none !important;
}
#header {
  display: flex;
  justify-content: center;
}
#header center{
  padding-top: 20px;
  display: flex;
  align-items: end;
}
#header img {
  margin-right: 10px !important;
  margin-left: 10px !important;
}
.logo {
  width: 35px !important;
  height: 40px !important;
}
.logo_title {
  height: 30px !important;
}
#page_refresh {
  position: absolute;
  top: 13px;
  right: 11px;
  background-color: #2F3E1D;
  border-radius: 5px;
}
#page_refresh:hover {
  cursor: pointer;
}
.refresh_btn {
  width: 36px;
  height: 36px;
  background-color: unset !important;
  display: flex;
  justify-content: center;
}
.refresh_btn img {
  width: 17px;
}
#component-0 {
  position: static;
}

.user, .assistant {
  background: transparent !important;
  font-size: 16px !important;
  width: 100% !important;
  border-radius: 4px !important;
  padding: 20px !important;
  margin-top: 10px;
}
.user {
  margin-top: 10px;
}
.assistant {
  background: #3b4b28 !important;
}
.chat_content {
  height: calc(100vh - 60px - 125px);
  overflow-y: auto;
}
.chat_content::-webkit-scrollbar {
  display: none;
}
.chat_content {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
#chatbot_container {
  padding: 10px 20px;
}
.chat_text p{
  color: #F8E8D2 !important;
  margin-bottom: unset !important;
}
.chat_text{
  display: flex;
  justify-content: space-between;
}
.feedback_btns{
  display: flex;
  align-items: start;
}
.feedback_btns:hover {
  cursor: pointer;
}
.feedback_btns img{
  width: 16px;
  min-width: 16px;
  margin: 5px;
}
#input_container .form{
  background: #28351b !important;
  border: unset;
}

#input_content {
  margin: 20px 20px 25px 20px!important;
  width: calc(100% - 40px) !important;
}
#input_content textarea {
  background-color: #3b4b28;
  border: unset;
  border-radius: 4px;
  color: #E5DFC8;
  font-size: 16px;
  padding: 10px 160px 10px 10px;
  --ring-color: none !important;
}
#input_content textarea:hover {
    border: unset;
}
#input_container {
  position: absolute;
  bottom: -55px;
  flex-direction: column;
  border-top: 1px solid rgba(212, 187, 152, 0.1);
  background: #28351b;
}
#input_send_btn {
  position: absolute;
  right: 60px;
  top: 30px;
  background-image: url(file/public/enter.svg) !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  height: 20px;
  min-width: unset;
  border: unset;
  box-shadow: unset !important;
}
#input_record_btn {
  position: absolute;
  right: 15px;
  top: 10px;
  background: transparent !important;
}
.input_buttons img {
  width: 20px;
  height: 20px;
  margin: 10px;
}
.input_buttons {
  background-color: transparent;
}
.input_buttons:hover {
  cursor: pointer;
}
#modal_close_btn {
  position: absolute;
  top: 14px;
  right: 26px;
}
#modal_close_btn:hover {
  cursor: pointer;
}
.close_button {
  width: 20px;
}

#record_modal {
  display: none;
  position: absolute !important;
  bottom: -54px;
  z-index: 10;
  padding: 20px;
  flex-direction: column;
  background: #28351b;
  border-top: 1px solid rgba(212, 187, 152, 0.1);
}
#listentitle h2{
  color: #F8E8D2 !important;
}
#listentitle center{
  color: #F8E8D2 !important;
  opacity: 0.5;
}
#component-19 {
  justify-content: center;
}
#modal_record_btn {
  display: flex;
  justify-content: center;
  background-image: url(file/public/circle.svg);
  background-repeat: no-repeat;
  background-size: contain;
  height: 60px;
  border: unset;
  margin-top: 20px;
  max-width: 60px;
  min-width: 60px;
}
.modal_record_button {
  width: 70px;
  height: 70px;
}

#feedback_modal {
  display: none;
  position: absolute !important;
  z-index: 10;
  height: 100vh !important;
  background: #28351b;
}
#feedbacktitle {
  padding-top: 26px;
}
#feedbacktitle center {
  color: #E5DFC8 !important;
  font-size: 24px !important;
}
#feedback_input_container {
  flex-direction: column;
  align-items: end;
  margin-top: 36px;
}
#feedback_input_container .form{
  background: transparent !important;
  border: unset !important;
}
#feedback_input_container button {
  width: fit-content !important;
  margin-right: 40px !important;
}

#download_modal {
  display: none;
  position: absolute !important;
  z-index: 10;
  height: 100vh !important;
  background: #28351b;
}
#downloadtitle {
  padding-top: 26px;
}
#downloadtitle center {
  color: #E5DFC8 !important;
  font-size: 24px !important;
}
#download_input_container {
  flex-direction: column;
  align-items: end;
  margin-top: 30px;
}
#download_input_container button {
  width: fit-content !important;
  margin-right: 40px !important;
}
#download_label h3{
  color: #E5DFC8 !important;
  margin-left: 20px;
}
#download_input_container .form{
  background: #28351b !important;
  border: unset !important;
  
}
#modal_input {
  margin: 0 20px 24px 20px !important;
  width: calc(100% - 40px) !important;
}
#modal_input textarea {
  background-color: #3b4b28;
  border: 1px solid #d4bb9820;
  border-radius: 4px;
  color: #E5DFC8;
  font-size: 16px;
  padding: 10px;
  box-shadow: unset;
}
#submodal_show_btn {
  padding: unset;
  height: 20px;
  min-width: 20px;
  max-width: 20px;
  border: unset;
}
#submodal {
  position: relative !important;
  bottom: -53px;
  display: flex;
  justify-content: center;
}
.arrow_button {
  width: 20px;
  background: transparent !important;
}
.arrow_button:hover {
  cursor: pointer;
}
.download_button_container {
  width: 170px;
  height: 50px;
  background: #DDAA0E !important;
  padding: 10px 20px;
  display: flex;
}
.download_button_container img {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}
.download_button_container h5, h3{
  color: #2F3E1D !important;
}
.download_button_text {
  background: unset !important;
}
.download_button_text h5{
  font-size: 11px !important;
  margin: unset !important;
}
.download_button_text h3{
  font-size: 17px !important;
  margin: unset !important;
}
#download_submodal {
  display: none;
  margin-bottom: 20px;
}
#download_submodal center {
  color: #E5DFC8 !important;
}
#appstore, #googleplay {
  display: flex;
  justify-content: center;
}
#appstore:hover {
  cursor: pointer;
}
#googleplay:hover {
  cursor: pointer;
}

#component-18 {
  width: 60px;
  min-width: unset;
  margin: auto;
}

#limit_modal {
  display: none;
  position: absolute !important;
  z-index: 10;
  height: 100% !important;
  background: #28351b;
}
.error_container {
  height: 100%;
  flex-direction: column;
  text-align: center;
}
.error_container img {
  width: 70px;
}
.error_container h3, h1{
  color: #F8E8D2 !important;
  margin: 20px !important;
}
.error_icon {
  display: flex;
  justify-content: center;
}
#error_modal_container{
  height: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

#virtual_element {
  display: none;
}
.meta-text-center {
  display: none !important;
}

#animation1 h3 {
  color: #E5DFC8 !important;
  position: relative;
  animation-name: anim1;
  animation-duration: 4s;
  animation-direction: reverse;
  right: -45%;
}

#animation2 h3 {
  color: #E5DFC8 !important;
  position: relative;
  animation-name: anim2;
  animation-duration: 4s;
  animation-direction: reverse;
  right: -45%;
}

#animation3 h3 {
  color: #E5DFC8 !important;
  position: relative;
  animation-name: anim3;
  animation-duration: 4s;
  animation-direction: reverse;
  right: -45%;
}

@keyframes anim1 {
  0% {
    bottom: 400px;
    opacity: 0;
    display: block;
  }
  50% {
    bottom: 400px;
    opacity: 0;
  }
  75% {
    bottom: 200px;
    opacity: 1;
  }
  100% {
    bottom: 0px;
    opacity: 0;
    display: block;
  }
}

@keyframes anim2 {
  0% {
    bottom: 400px;
    opacity: 0;
    display: none;
  }
  25% {
    bottom: 400px;
    opacity: 0;
  }
  50% {
    bottom: 200px;
    opacity: 1;
  }
  75% {
    bottom: 0px;
    opacity: 0;
  }
}

@keyframes anim3 {
  0% {
    bottom: 400px;
    opacity: 0;
    display: none;
  }
  25% {
    bottom: 200px;
    opacity: 1;
  }
  50% {
    bottom: 0px;
    opacity: 0;
  }
}
"""

class Message(BaseModel):
  role: str
  content: str
  
modal_show = False
  
def make_completion(messages:List[Message]):
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
  refresh_btn += "<img src='file/public/refresh.svg'/>"
  refresh_btn += "</div>"
  return refresh_btn

def predict(input):
  messages.append({"role": "user", "content": input})
  res = make_completion(messages)
  response = res.replace("\n\n", "\n")
  messages.append({"role": "assistant", "content": response})
  return chatbot_container()

def chatbot_container():
    chat_history = "<div class='chat_content'>"
    onclick = "let modalElement=document.getElementById(\"feedback_modal\"); modalElement.style.display=\"block\";"
    for index, msg in enumerate(messages):
      if msg["role"] == "user":
        chat_history += "<div id='array_{}' class='chat_text {}'>{}</div>".format(index, msg["role"], markdown.markdown(msg["content"], output_format='html5'))
      elif msg["role"] == "assistant":
        chat_history += "<div id='array_{}' class='chat_text {}'>{}<div class='feedback_btns' onclick='{}'><img src='file/public/like.svg'/><img src='file/public/dislike.svg'/></div></div>".format(index, msg["role"], markdown.markdown(msg["content"], output_format='html5'), onclick)
    chat_history += "</div>"
    return chat_history

def msg_send_btn():
  onclick = "let modalElement=document.getElementById(\"input_record_btn\"); modalElement.style.display=\"none\"; let modalElement=document.getElementById(\"input_send_btn\"); modalElement.style.right=\"15px\";"
  msg_send_btn = "<div class='input_buttons' onclick='{}'>".format(onclick)
  msg_send_btn += "<img src='file/public/enter.svg'/>"
  msg_send_btn += "</div>"
  return msg_send_btn
  
def msg_record_btn():
  onclick = "let modalElement=document.getElementById(\"record_modal\"); modalElement.style.display=\"block\"; let contentElement=document.getElementById(\"chat_content\"); contentElement.style.height=\"calc(100vh - 60px - 170px)\";"
  msg_record_btn = "<div class='input_buttons' onclick='{}'>".format(onclick)
  msg_record_btn += "<img src='file/public/record.svg'/>"
  msg_record_btn += "</div>"
  return msg_record_btn

def modal_record_btn():
  print("Recording started...")
  # frames = []
  # while True:
  #   data = stream.read(1024)
  #   frames.append(data)
  #   if len(frames) > 16000 / 1024 * 5: # Record voice for 5 seconds (can be adjusted) 
  #     break
  # stream.stop_stream()
  # stream.close()
  # audio.terminate()

  # wf = wave.open("recorded_voice.wav", 'wb')
  # wf.setnchannels(1)
  # wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
  # wf.setframerate(16000)
  # wf.writeframes(b''.join(frames))
  # wf.close()
  
  # print("Transcribing...")
  # audio_file= open("recorded_voice.wav", "rb")
  # transcript = openai.Audio.transcribe("whisper-1", audio_file)
  # return predict(transcript["text"])
  
def record_modal_close_btn():
  onclick = "let modalElement = document.getElementById(\"record_modal\"); modalElement.style.display=\"none\"; let contentElement=document.getElementById(\"chat_content\"); contentElement.style.height=\"calc(100vh - 60px - 110px)\";"
  close_button = "<div class='close_button' onclick='{}'>".format(onclick)
  close_button += "<img src='file/public/close.svg'/>"
  close_button += "</div>"
  return close_button

def feedback_modal_close_btn():
  onclick = "let modalElement = document.getElementById(\"feedback_modal\"); modalElement.style.display=\"none\";"
  close_button = "<div class='close_button' onclick='{}'>".format(onclick)
  close_button += "<img src='file/public/close.svg'/>"
  close_button += "</div>"
  return close_button

def download_modal_close_btn():
  onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"none\";"
  close_button = "<div class='close_button' onclick='{}'>".format(onclick)
  close_button += "<img src='file/public/close.svg'/>"
  close_button += "</div>"
  return close_button

def limit_modal_close_btn():
  onclick = "let modalElement = document.getElementById(\"limit_modal\"); modalElement.style.display=\"none\";"
  close_button = "<div class='close_button' onclick='{}'>".format(onclick)
  close_button += "<img src='file/public/close.svg'/>"
  close_button += "</div>"
  return close_button

def download_submodal_show_btn():
  onclick = "let virtual_element = document.getElementById(\"virtual_element\");let state = virtual_element.querySelector(\"p\").innerHTML;let modalElement = document.getElementById(\"download_submodal\");let imgElement = document.querySelector(\".arrow_button img\");let arrowElement = document.getElementById(\"submodal_show_btn\");state == \"true\" ? (modalElement.style.display=\"block\", arrowElement.style.bottom=\"90px\", virtual_element.querySelector(\"p\").innerHTML=\"false\", imgElement.setAttribute(\"src\", \"file/public/down_arrow.svg\")) : (modalElement.style.display=\"none\",arrowElement.style.bottom=\"0\", virtual_element.querySelector(\"p\").innerHTML=\"true\", imgElement.setAttribute(\"src\", \"file/public/up_arrow.svg\"));"
  show_button = "<div class='arrow_button' onclick='{}'>".format(onclick)
  show_button += "<img src='file/public/up_arrow.svg'/>"
  show_button += "</div>"
  return show_button

def sendFeedback(input):
  print("feedback----", input)
    
def submitDownload(input):
  print("download----", input)
  
def AppStore ():
  onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"block\";"
  appstore = "<div class='download_button_container' onclick='{}'>".format(onclick)
  appstore += "<img src='file/public/appstore.svg'/>"
  appstore += "<div class='download_button_text'><h5>Download on the</h5><h3>App Store</h3></div>"
  appstore += "</div>"
  return appstore
  
def GooglePlay ():
  onclick = "let modalElement = document.getElementById(\"download_modal\"); modalElement.style.display=\"block\";"
  google = "<div class='download_button_container' onclick='{}'>".format(onclick)
  google += "<img src='file/public/google.svg'/>"
  google += "<div class='download_button_text'><h5>GET IT ON</h5><h3>Google Play</h3></div>"
  google += "</div>"
  return google

def error_modal():
  error = "<div class='error_container'>"
  error += "<div class='error_icon'><img src='file/public/error.svg'/></div>"
  error += "<h1>Oops!</h1>"
  error += "<h3>Sorry, we're experiencing high traffic.</h3>"
  error += "<h3>Please try again later</h3>"
  error += "</div>"
  return error

gr.HTML(value="<script>document.getElementById('submodal').addEventListener('click', displayDate);function displayDate() {alert(123);}</script>")
with gr.Blocks(css=css) as demo:
  logger.info("Starting Demo...")

  with gr.Row():
    header = gr.Markdown(value="""<center><img src="file/public/face.jpg" class="logo"/><img src="file/public/title.svg" class="logo_title"/></center>""", elem_id="header")
  gr.HTML(value=page_refresh, elem_id="page_refresh")
  chatbot = gr.HTML(value=chatbot_container, elem_id="chatbot_container")

  with gr.Row(elem_id="input_container"):
    txt = gr.Textbox(show_label=False, max_lines=5, placeholder="How do you feel today?", elem_id="input_content").style(container=False)
    send_btn = gr.Button("", elem_id="input_send_btn")
    send_btn.click(fn=predict, inputs=[txt], outputs=[chatbot])
    # gr.HTML(value=msg_send_btn, elem_id="input_send_btn")
    gr.HTML(value=msg_record_btn, elem_id="input_record_btn")
    with gr.Row(elem_id="download_submodal"):
      gr.Markdown(value="""<h5><center>Download the app</center></h5>""", elem_id="footer")
      with gr.Row(elem_id="download_submodal_content"):
        gr.HTML(value=AppStore, elem_id="appstore")
        gr.HTML(value=GooglePlay, elem_id="googleplay")
  txt.submit(predict, inputs=[txt], outputs=[chatbot])
  
  with gr.Row(elem_id="record_modal"):
    with gr.Row():
      listen_title = gr.Markdown(value="""<h2><center>Listening</center></h2>""", elem_id="listentitle")
    with gr.Row():
      recording = gr.Button("", elem_id="modal_record_btn")
      # recording.click(fn=modal_record_btn, outputs=[chatbot])
    gr.HTML(value=record_modal_close_btn, elem_id="modal_close_btn")
    
  with gr.Row(elem_id="feedback_modal"):
    with gr.Row():
      listen_title = gr.Markdown(value="""<h3><center>Rating feedback</center></h3>""", elem_id="feedbacktitle")
    with gr.Row(elem_id="feedback_input_container"):
      with gr.Row():
        txt_feedback = gr.Textbox(show_label=False, lines=3, placeholder="What do you dislike about the response?", elem_id="modal_input").style(container=False)
      send_feedback = gr.Button(value="Submit feedback")
      send_feedback.click(fn=sendFeedback, inputs=txt_feedback)
    gr.HTML(value=feedback_modal_close_btn, elem_id="modal_close_btn")

  with gr.Row(elem_id="download_modal"):
    with gr.Row():
      listen_title = gr.Markdown(value="""<h3><center>We're on it!</center></h3>""", elem_id="downloadtitle")
    with gr.Row(elem_id="download_input_container"):
      gr.Markdown(value="""<h3>Leave your email to get notified once the app is available in your country</h3>""", elem_id="download_label")
      with gr.Row():
        txt_download = gr.Textbox(show_label=False, lines=1, placeholder="hi@email.com", elem_id="modal_input").style(container=False)
      submit_download = gr.Button(value="Submit")
      submit_download.click(fn=submitDownload, inputs=txt_download)
    gr.HTML(value=download_modal_close_btn, elem_id="modal_close_btn")
    
  with gr.Row(elem_id="limit_modal"):
    gr.HTML(value=error_modal, elem_id="error_modal_container")
    gr.HTML(value=limit_modal_close_btn, elem_id="modal_close_btn")
  
  with gr.Row(elem_id="submodal"):
    submodalbtn = gr.HTML(value=download_submodal_show_btn, elem_id="submodal_show_btn")
  # gr.HTML(value="<h3>Hello there!</h3>", elem_id="animation1")
  # gr.HTML(value="<h3>My name is Alfred Penny</h3>", elem_id="animation2")
  # gr.HTML(value="<h3>At your service...</h3>", elem_id="animation3")
  gr.HTML(value="<p>true</p>", elem_id="virtual_element")

demo.launch(server_port=8080)