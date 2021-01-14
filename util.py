import os


# Read files in the negative folder and generates neg.txt
def generate_negative_description_file():
    # Open and overwrite all existing data in file
    with open('neg.txt', 'w') as f:
        # Loop over filenames
        for filename in os.listdir('negative'):
            f.write(f'negative/{filename}\n')


generate_negative_description_file()
