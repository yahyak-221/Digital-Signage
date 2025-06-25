import json
import datetime
def log_video_played(video_title):
    # Define the log entry
    log_entry = {
        'timestamp': str(datetime.datetime.now()),
        'video_title': video_title
    }

    # Load existing log file if it exists
    try:
        with open('video_log.json', 'r') as log_file:
            log_data = json.load(log_file)
    except FileNotFoundError:
        log_data = []

    # Append the new log entry
    log_data.append(log_entry)

    # Save the updated log file
    with open('video_log.json', 'w') as log_file:
        json.dump(log_data, log_file, indent=4)


# Example usage
video_title = 'Sample Video 1'
log_video_played(video_title)