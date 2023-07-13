import threading
import os
import sys
import shutil
import music_tag
import time
import datetime
import pyautogui

# Audio file extensions to be searched
formats = ['.aac', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.wav']

# Remove Windows-restricted file name characters
def remove_restricted_chars(string):
    restricted_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in restricted_chars:
        string = string.replace(char, '')
    return string

# Copy all files from source directory to destination directory
def copy_files(source, destination):
    track_count = 0
    for root, dirs, files in os.walk(source):
        for name in files:
            if name.endswith(tuple(formats)):
                track_count += 1
                file_path = os.path.join(root, name)  # Original file path
                print('Found track:', file_path)
                track = music_tag.load_file(file_path)
                album_artist = remove_restricted_chars(str(track['albumartist']))
                album = remove_restricted_chars(str(track['album']))
                new_dir = os.path.join(destination, str(track['year']), f"{album_artist} - {album}")
                new_file_path = os.path.join(new_dir, name)
                os.makedirs(new_dir, exist_ok=True)
                if not os.path.exists(new_file_path):
                    shutil.copy2(file_path, new_file_path)
    print(f"{track_count} tracks found in {source}\n")

# Trigger a screenshot in a specific time interval
def print_screen():
    while take_screenshots:
        time.sleep(0.01)
        new_screenshot = pyautogui.screenshot()
        screenshot_name = str(datetime.datetime.now()) + ".png"
        screenshot_path = os.path.join("Screenshots", remove_restricted_chars(screenshot_name))
        new_screenshot.save(screenshot_path)

# Create new music directory
dir_path = os.path.join(os.getcwd(), 'Sorted Music')

# Remove directory if it exists
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)

# Change current working directory to Sorted Music
os.mkdir(dir_path)
os.chdir(dir_path)

# Create directory for screenshots
os.makedirs("Screenshots", exist_ok=True)
take_screenshots = True

# Run Print Screen on a new thread
t1 = threading.Thread(target=print_screen)
t1.start()

print('-- Music Sorter --\n')

print('Searching for tracks in Documents directory...')
copy_files(os.path.expanduser('~') + '\\Documents', dir_path)

print('Searching for tracks in Desktop directory...')
copy_files(os.path.expanduser('~') + '\\Desktop', dir_path)

# Stop taking screenshots
take_screenshots = False



# Wait for thread to finish execution
t1.join()
