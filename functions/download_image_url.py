import urllib.request
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')



def download_image_url(image_url, photo_folder, image_name):
    os.makedirs(photo_folder, exist_ok=True)
    image_path = os.path.join(photo_folder, image_name)

    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()
    except Exception as e:
        print(f"Failed to download image {image_name}: {e}")
        return
    
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)   
