from datetime import datetime
import cv2
import subprocess
import time
import platform
import socket
import requests
import os
import keyboard
import json
import pyautogui



################################ READ ME FIRST ################################  

# Here in the below we have different function to do the different jobs 
# function for getting the duration of video, function for checking the wifi connectivity, function for  downloading the video from the given API, function for maintaining the log for each video, function for taking the screenshot(note: it work on windows on RASPBERRY it's only taking the screenshot of terminal), function for maintaining the videos which are in the API which will only play them(because other's end time has meet),  and then the final function play_video which will play the vidoes and combine all the function to work everything properly
## Few changes are needed to work the same on the RASPBERRY such changing the directory path and instead of VLC we have to go omxplayer
# This code will work properly only and only if the videos are available in the API

################################ That's sit till now ##############################




#Function for getting the duration of the video so that we can hold the screen
def get_video_length(video_path):
    try:
        capture = cv2.VideoCapture(video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps != 0 else 0
        capture.release()
        return duration - 0.3
    except Exception as e:
        print(f"Error: {e}")
        return None
################################  



#Function to check wifi connectivity
def check_wifi_connectivity():
    try: