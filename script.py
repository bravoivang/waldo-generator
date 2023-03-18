import os
import random
from PIL import Image

# Set source and output directories
SOURCE_DIR = 'source'
OUTPUT_DIR = 'output'

# Get list of subdirectories in source directory sorted by index from name
subdirs = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(
    os.path.join(SOURCE_DIR, d))], key=lambda x: int(x[:2]))
print('Processed subdirectories:', ', '.join(subdirs))


def filter_existing_files(file_list):
    valid_extensions = {'.png'}
    valid_files = []

    for file_name in file_list:
        file_path = os.path.join(subdir_path, file_name)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_name)
            if file_extension.lower() in valid_extensions:
                valid_files.append(file_name)

    return valid_files


# Get list of image files in each subdirectory
image_files = {}
for subdir in subdirs:
    subdir_path = os.path.join(SOURCE_DIR, subdir)
    image_files[subdir] = [os.path.join(subdir_path, f) for f in os.listdir(
        subdir_path) if f.endswith('.png')]

# Get dimensions of first image in first subdirectory
first_image = Image.open(image_files[subdirs[0]][0])
image_width, image_height = first_image.size

# Generate 10 new images
# combinations = set()  # create an empty set to store combinations TODO: avoid duplicates
for i in range(20):
    # Choose random image from each subdirectory (if available)
    random_images = {}
    used_model = None
    for subdir in subdirs:
        # This is the folder 00_faces: it is the one who tells the model
        subdir_path = os.path.join(SOURCE_DIR, "01_faces")
        random_file = random.choice(
            filter_existing_files(os.listdir(subdir_path)))
        used_model = random_file.split('_')[0]
        if len(image_files[subdir]) > 0:
            if ('opt' in subdir) and (random.random() < 0.72):
                print('folder not-used:', subdir)
                continue

            subdir_path = os.path.join(SOURCE_DIR, subdir)
            filtered_files = filter_existing_files([f for f in os.listdir(
                subdir_path) if (f.startswith(used_model + '_') or f.startswith('T_'))])
            if len(filtered_files) == 0:
                raise ValueError(
                    "The files in the folder {subdir} have a wrong format!")
            random_file = random.choice(filtered_files)
            random_images[subdir] = Image.open(
                os.path.join(subdir_path, random_file))
            # print('Image selected:', random_file)

    # Create new blank image
    new_image = Image.new(
        'RGBA', (image_width, image_height), (255, 255, 255, 0))

    # Paste random images onto new image
    for subdir in subdirs:
        if subdir in random_images:
            new_image.paste(random_images[subdir],
                            (0, 0), random_images[subdir])

    # Save new image
    output_filename = 'output_{}.png'.format(i)
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    new_image.save(output_path)
