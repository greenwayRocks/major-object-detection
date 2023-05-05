from django.shortcuts import render
from django.http import StreamingHttpResponse, FileResponse, HttpResponse
import yolov5
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_boxes, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
import cv2
from PIL import Image as im
import torch
from yolov5.utils.general import *

# s2t
import pyttsx3
from gtts import gTTS
import requests
import base64
# from pydub import AudioSegment
from io import BytesIO

# def text_to_speech(request, text):
    # Create a gTTS object and specify the language
    # tts = gTTS(text=text, lang='en')

    # Save the audio file to a buffer
    # audio_file = BytesIO()
    # tts.write_to_fp(audio_file)

    # Convert the audio file to a base64-encoded string
    # encoded_audio = base64.b64encode(audio_file.getvalue()).decode('utf-8')

    # Create an HTML5 audio element that plays the base64-encoded audio
    # audio_player = '<audio controls><source src="data:audio/mpeg;base64,%s" type="audio/mpeg"></audio>' % encoded_audio

    # Return the HTML5 audio player as a Django HttpResponse
    #return HttpResponse(audio_player)


def text_to_speech(request, text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set the engine properties
    engine.setProperty('rate', 150)  # Speed in words per minute
    engine.setProperty('volume', 0.9)  # Volume of the speech

    # Generate speech from the text
    engine.say(text)
    engine.runAndWait()

    # Return an empty HTTP response
    return HttpResponse()


# def text_to_speech(text):
#     # text = request.GET.get('text')
#     audio = generate_audio(text)
#     audio_bytes = BytesIO()
#     audio.export(audio_bytes, format='mp3')
#     audio_url = f"data:audio/mp3;base64,{base64.b64encode(audio_bytes.getvalue()).decode()}"
#     return JsonResponse({'audio_url': audio_url})


def speak_objects(objects):
    engine = pyttsx3.init()
    # Set the engine properties
    engine.setProperty('rate', 150) # Set the speaking rate
    engine.setProperty('voice', 'english-us') # Set the voice

    # Convert the text to speech
    text = objects[0]
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

    # Serve the audio file
    file_path = os.path.join(os.getcwd(), 'output.mp3')
    return FileResponse(open(file_path, 'rb'))
    text = "I see the following objects: "
    for obj in objects:
         text += obj + ", "
         engine.say(text)
         engine.runAndWait()
                    
         tts = gTTS(text=text, lang='en')
         tts.save("detected_objects.mp3")
         os.system("mpg321 detected_objects.mp3")

# Create your views here.
def index(request):
    return render(request,'index.html')

model = yolov5.load('last.pt')
# model = yolov5.load('yolov5s.pt')
# model = yolov5.load('best.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
device = select_device('cpu') # 0 for gpu, '' for cpu

# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names
hide_labels=False
hide_conf = False

def stream(request):
    # address = "https://192.168.20.75:8080/video"
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(address)
    model.conf = 0.25
    model.iou = 0.5
   # model.classes = [0,64,39]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break

        results = model(frame, augment=True)
        # proccess
        annotator = Annotator(frame, line_width=2, pil=not ascii) 
        det = results.pred[0]
        if det is not None and len(det):  
            for *xyxy, conf, cls in reversed(det):
                # classy_class = set()
                c = int(cls)  # integer class
                label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                get_class = label.split()
                target = get_class[0]
                print(target)

                text_to_speech(request, target)
                # speak_objects(final_objs)
                # classy_class.add(classy)
                annotator.box_label(xyxy, label, color=colors(c, True)) 

        im0 = annotator.result()

        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        # final_objs = list(classy_class)

        # speak_objects(final_objs)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

def video_feed(request):
    return StreamingHttpResponse(stream(request), content_type='multipart/x-mixed-replace; boundary=frame')    


def index(request):
    return render(request,'index.html')


# def video_feed(request):
#     return StreamingHttpResponse(stream(),content_type='multipart/x-mixed-replace; boundary=frame')

# def stream():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret,frame = cap.read()
#         if not ret:
#             print('failed to read camera')
#         img_bytes = cv2.imencode('.jpg',frame)[1].tobytes()
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ img_bytes +b'\r\n')
