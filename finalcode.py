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
        # Attempt a connection to a well-known server (google.com) on port 80
        socket.create_connection(("google.com", 80), timeout=1)
        return True
    except OSError:
        return False
################################  



#Function to download the videos from the API
def download_video():
    if check_wifi_connectivity():
        print("Wi-Fi is connected.")
        api_url = "https://debugzone.live/fx-screen-manager/screenAPI.php"
        video_files = []

        # Specify the directory to save the videos
        save_directory = "C:/Users/sahil/Desktop/pythonexp/videos/"

        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            videos = response.json()
            existed_video_array = []
            
            # Iterate through the videos
            for video in videos:
                # Get the video URL and other attributes
                id = video['id']
                video_url = video['videoLink']
                video_name = video['brandName']
                
                video_file_name = id + video_name + '.mp4'
                video_file_path = os.path.join(save_directory, video_file_name)
                new_videopath = f"C:/Users/sahil/Desktop/pythonexp/videos/{video_file_name}" 
                

                existed_video = f"{os.path.splitext(os.path.basename(new_videopath))[0]}" + ".mp4"
                existed_video_array.append(existed_video)

                video_files.append(new_videopath)
                # Check if the video has already been downloaded
                if os.path.exists(video_file_path):
                    print(f"Video '{video_file_name}' already exists. Skipping...")
                    continue

                # Download the video
                video_file = requests.get(video_url)

                # Save the video to a file
                with open(video_file_path, 'wb') as f:
                    f.write(video_file.content)

                print(f"Downloaded video: {video_file_name}")

            print(f"Existed video array: {existed_video_array}")
            delete_specific_videos(save_directory, existed_video_array)


        else:
            print("Error occurred while accessing the API.")

    else:
        print("Wi-Fi is not connected.")
    ################################   
################################  



#Function to delete video from the folders
def delete_specific_videos(folder_path, videos_to_keep):
    video_extensions = ['.mp4', '.avi', '.mkv']

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in video_extensions and file not in videos_to_keep:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
################################  


        

#Function to maintain the logs of the video
def store_video_data(video_name, start_time, end_time):
    # Function to store video data in JSON file
    data = {
        "video_name": video_name,
        "start_time": start_time,
        "end_time": end_time
    }
    
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            try:
                video_data = json.load(file)
            except json.JSONDecodeError:
                video_data = []
    else:
        video_data = []
    
    video_data.append(data)
    
    with open('data.json', 'w') as file:
        json.dump(video_data, file)
################################   



#Function to take screenshots after specific intervals of time
def capture_screenshots(folder_path, s_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Capture and save screenshots
    screenshot = pyautogui.screenshot()
    # Save the screenshot to a file with a unique name
    file_name = f"{s_name}.png"
    file_path = os.path.join(folder_path, file_name)
    screenshot.save(file_path)
    print("Screenshot saved:", file_path)
################################   
    

#Function for playing the videos in loop 
def play_videos(i):
    try:
        while True:
            download_video()
            new_video_path = []
            screenshot_folder = "C:/Users/sahil/Desktop/pythonexp/screenshots/"
            j = 0

            main_folder_path = "C:/Users/sahil/Desktop/pythonexp/videos/"
            for file_name in os.listdir(main_folder_path):
                file_path = os.path.join(main_folder_path, file_name)
                # print(file_path)
                if(os.path.isfile(file_path)) and (file_name.lower().endswith(".mp4")):
                    new_video_path.append(file_path)
                print(new_video_path)
            ################################    

            for video_file in new_video_path:
                # print(video_file)
                # ss_name = f"{os.path.splitext(os.path.basename(video_file))[0]}_{i}_{j}"
                # ss_name = f"{os.path.splitext(os.path.basename(video_file))[0]}"
                # print(ss_name)
                ss_name = f"Screenshot_{i}_{j}"
                # print(ss_name)
                
                if platform.system() == 'Windows':
                    # Launch the default media player on Windows to play the video
                    subprocess.Popen(['start', '', video_file], shell=True)
                elif platform.system() == 'Linux':
                    # Launch VLC on Linux to play the video
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cmd = f"omxplayer -o hdmi {video_file}"
                    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print("Video playback started:", video_file)
                lenght = get_video_length(video_file)
                print(lenght)
                time.sleep(int(lenght)) 
                time.sleep(lenght)  # Adjust sleep time as necessary for your video duration
                capture_screenshots(screenshot_folder, ss_name)
                store_video_data(video_file, start_time, end_time)
                j = j+1
            i = i+1
                
    except Exception as e:
        print("An error occurred:", e)
################################   
 
counter = 0

play_videos(counter)
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# videoplay
import os
import time
def play_videos(video_files):
    try:
        for video_file in video_files:
            # Open each video file using the default media player in Windows
            os.startfile(video_file)
            print("Video playback started:", video_file)
            # input("Press Enter to play the next video...")
            time.sleep(19)
    except Exception as e:
        print("An error occurred:", e)

# Provide a list of video files to play
video_files = [
    r'C:/Users/sahil/Desktop/pythonexp/2Hertzsoft.mp4',
    r'C:/Users/sahil/Desktop/pythonexp/1Maybelline.mp4'
]

# Call the function to play the videos
play_videos(video_files)