import os


# Change directory paths to rename all files inside
directory = r'C:\Users\nguye\Documents\Projects\audiosurf-bot\negative_block\Blocks'

# Rename screenshot raw_images starting from 0
img_count = 350
extension = '.jpg'
for img in os.listdir(directory):
    if img.endswith(extension):
        os.rename(os.path.join(directory, img),
                  os.path.join(directory, f'{img_count}.jpg'))
        img_count += 1
