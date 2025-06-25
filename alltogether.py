from datetime import datetime
import cv2
import subprocess
import time
import platform
import requests
import os

# JSON API endpoint
api_url = "https://debugzone.live/fx-screen-manager/screenAPI.php"
video_files = []

# Specify the directory to save the videos
save_directory = "C:/Users/sahil/Desktop/pythonexp"

# Make a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    videos = response.json()
    
    # Iterate through the videos
    for video in videos:
        # Get the video URL and other attributes
        id = video['id']
        video_url = video['videoLink']
        video_name = video['brandName']
        video_file_name = id + video_name + '.mp4'
        video_file_path = os.path.join(save_directory, video_file_name)
        new_videopath = f"C:/Users/sahil/Desktop/pythonexp/{video_file_name}" 
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

else:
    print("Error occurred while accessing the API.")
   
   

def get_video_length(video_path):
    try:
        capture = cv2.VideoCapture(video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps != 0 else 0
        capture.release()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None

def play_videos(video_files, end_date):
    try:
        while datetime.now() < end_date:
            for video_file in video_files:
                print("current time: ", datetime.now())
                print("End time: ", end_date)
                if platform.system() == 'Windows':
                    # Launch the default media player on Windows to play the video
                    subprocess.Popen(['start', '', video_file], shell=True)
                elif platform.system() == 'Linux':
                    # Launch VLC on Linux to play the video
                    subprocess.Popen(['vlc', video_file])
                print("Video playback started:", video_file)
                lenght = get_video_length(video_file)
                print(int(lenght))
                time.sleep(int(lenght))  # Adjust sleep time as necessary for your video duration
                # time.sleep(20)
    except Exception as e:
        print("An error occurred:", e)

print(video_files)
end_date = datetime(2023, 6, 28, 18,24)
# Call the function to play the videos
play_videos(video_files, end_date)