# Django-YOLOV5-real-time-object-detection-

You look only once (YOLO) is the best and the fast object detection algorithm in real time. this is a django project where i used yolov5 for object detection using the webcam. the detected objects or the resulting frames will be streaming in the html page on realtime. there will be an API video_feed where we can see the realtime detections. 

Installation (Use bash/Git bash shell):

```bash
$ git clone https://github.com/greenwayRocks/major-object-detection

$ cd major-object-detection

$ python -V
$ # check if python version > 3

$ python -m venv .env

$ source .env/bin/activate

$ pip install -r requirements.txt

$ which python
$ # to check if python's running from the created env

$ python manage.py runserver
```
