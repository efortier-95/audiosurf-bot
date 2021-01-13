import os

# Rename screenshot images starting from 0
img_count = 0
extension = '.jpg'
directory = r'C:\Users\nguye\Documents\Projects\audiosurf-bot\negative'
for img in os.listdir(directory):
    if img.endswith(extension):
        os.rename(os.path.join(directory, img),
                  os.path.join(directory, f'{img_count}.jpg'))
        img_count += 1
