import os


directory = r'C:\Users\nguye\Documents\Projects\audiosurf-bot\negative_block\Blocks'
img_count = 0


# Rename screenshot images
def rename_img(path, count):
    for img in os.listdir(path):
        if img.endswith('.jpg'):
            os.rename(os.path.join(directory, img),
                      os.path.join(directory, f'{count}.jpg'))
            count += 1


filename = 'neg_block.txt'


# Read files in the negative_block folder and generates negative file
def generate_negative_description_file(fname):
    # Open and overwrite all existing data in file
    with open('neg_block.txt', 'w') as f:
        # Loop over filenames
        for fname in os.listdir('negative_block'):
            f.write(f'negative_block/{filename}\n')
