import urllib.request
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Download an image from a URL and save it to the specified folder with the given name
def download_image_url(image_url, photo_folder, image_name):
    os.makedirs(photo_folder, exist_ok=True)
    image_path = os.path.join(photo_folder, image_name)

    # Download the image data
    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()
    except Exception as e:
        print(f"Failed to download image {image_name}: {e}")
        return
    
    # Save the image data to a file
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)   
