import os


# Change when renaming different directory
img_dir = r'C:\Users\nguye\Documents\Projects\audiosurf-bot\positive_power'
img_count = 0


# Rename screenshot images
def rename_img(path, count):
    for img in os.listdir(path):
        if img.endswith('.jpg'):
            os.rename(os.path.join(img_dir, img),
                      os.path.join(img_dir, f'{count}.jpg'))
            count += 1


# Change when training different cascade
neg_dir = 'negative_block'
filename = 'training_data/neg_block.txt'


# Read files in the negative directory and generates negative file
def generate_negative_description_file(path, name):
    # Open and overwrite all existing data in file
    with open(name, 'w') as f:
        # Loop over filenames
        for fname in os.listdir(path):
            f.write(f'{neg_dir}/{fname}\n')


# rename_img(img_dir, img_count)
# generate_negative_description_file(neg_dir, filename)
