from datetime import datetime
import cv2
import subprocess
import time
import platform

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


# Provide a list of video files to play
video_files = [
    'C:/Users/YayhaKhan/Desktop/HACKCLUB/Animation.mp4',
    'C:/Users/YayhaKhan/Desktop/HACKCLUB/1Maybelline.mp4',
    'C:/Users/YayhaKhan/Desktop/HACKCLUB/2Hertzsoft.mp4'
]

end_date = datetime(2023, 6, 28, 15, 41)
# Call the function to play the videos
play_videos(video_files, end_date)
# 
# 
# 
# 
# 
# 
# 
# 