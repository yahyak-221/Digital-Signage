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
    r'./HACKCLUB/IOT/videos/2Hertzsoft.mp4',
    r'./HACKCLUB/IOT/videos/1Maybelline.mp4'
]

# Call the function to play the videos
play_videos(video_files)
