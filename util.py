import os


# Read files in the negative_block folder and generates neg_block.txt
# Change directory variable when training another cascade
def generate_negative_description_file():
    # Open and overwrite all existing data in file
    with open('neg_block.txt', 'w') as f:
        # Loop over filenames
        for filename in os.listdir('negative_block'):
            f.write(f'negative_block/{filename}\n')


generate_negative_description_file()
