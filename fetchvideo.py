# import requests
# api_url = "Your_API_URL"  # Replace with your API endpoint URL
# save_path = "C:/Users/YayhaKhan/Desktop/HACKCLUB/OUTPUT" # Replace with the desired save path and filename

# # Send GET request to the API endpoint
# def download_video(url, save_path):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(save_path, "wb") as file:
#             file.write(response.content)
#         print("Video downloaded successfully.")
#     else:
#         print("Failed to download video.")


# response = requests.get(api_url)

# if response.status_code == 200:
#     # Parse the JSON response
#     json_data = response.json()

#     # Iterate over each video object in the JSON data
#     for video in json_data:
#         if "videoLink" in video:
#             video_link = video["videoLink"]
#             # print(video_link)
#             download_video(video_link, save_path)
#         else:
#             print("Video Link parameter not found in the JSON data.")
# else:
#     print("Failed to retrieve data from the API.")

import requests
import os

# JSON API endpoint
api_url = "Your_API_URL" # Replace with your API endpoint URL

# Specify the directory to save the videos
save_directory = "/home/pi/Documents/iot"

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