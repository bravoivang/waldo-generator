import yaml
import random
from PIL import Image
import constants
import utils


def getConfig(path, name=constants.CONFIG_NAME):
    file_path = utils.join_path(path, name)
    if not utils.is_file(file_path):
        raise FileNotFoundError(f'The file "{file_path}" does not exist.')
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
        return config


def filter_existing_files(file_list):
    valid_extensions = {'.png'}
    valid_files = []

    for file_name in file_list:
        file_path = utils.join_path(subdir_path, file_name)
        if utils.is_file(file_path):
            _, file_extension = utils.split(file_name)
            if file_extension.lower() in valid_extensions:
                valid_files.append(file_name)

    return valid_files


# Get list of subdirectories in source directory
subdirs = [d for d in utils.list(constants.SOURCE_DIR) if utils.is_dir(
    utils.join_path(constants.SOURCE_DIR, d))]

print('Processed subdirectories:', ', '.join(subdirs))


# Get list of image files in each subdirectory
image_files = {}
for subdir in subdirs:
    subdir_path = utils.join_path(constants.SOURCE_DIR, subdir)
    image_files[subdir] = [utils.join_path(subdir_path, f) for f in utils.list(
        subdir_path) if f.endswith('.png')]

# Get dimensions of first image in first subdirectory and models
first_image = Image.open(image_files[subdirs[0]][0])
image_width, image_height = first_image.size
config = getConfig(constants.SOURCE_DIR, constants.INIT_CONFIG_NAME)
models = config[constants.INIT_CONFIR_ATTR_MODEL]
combinations = config[constants.INIT_CONFIR_ATTR_AMOUNT]


# combinations = set() # create an empty set to store combinations TODO: avoid duplicates
for i in range(combinations):
    # Choose random image from each subdirectory (if available)
    used_zindexes = set()
    random_images = {}
    used_model = random.choice(models)
    for subdir in subdirs:
        if len(image_files[subdir]) > 0:
            subdir_path = utils.join_path(constants.SOURCE_DIR, subdir)
            parameters = getConfig(subdir_path)
            probability = parameters[constants.CONFIR_ATTR_ODD]
            if random.random() < probability:
                continue

            z_index = parameters[constants.CONFIR_ATTR_INDEX]
            if z_index in used_zindexes:
                raise ValueError(f"zIndex {z_index} already used")

            filtered_files = filter_existing_files([f for f in utils.list(
                subdir_path) if (f.startswith(used_model + '_') or f.startswith('T_'))])
            if len(filtered_files) == 0:
                raise ValueError(
                    "The files in the folder {subdir} have a wrong format!")
            random_file = random.choice(filtered_files)
            random_images[z_index] = Image.open(
                utils.join_path(subdir_path, random_file))
            used_zindexes.add(z_index)

    # Create new blank image
    new_image = Image.new(
        'RGBA', (image_width, image_height), (255, 255, 255, 0))

    # Paste random images onto new image
    sorted_images = sorted(random_images.items())
    for zIndex, image in sorted_images:
        new_image.paste(image, (0, 0), image)

    # Save new image
    output_filename = 'output_{}.png'.format(i)
    output_path = utils.join_path(constants.OUTPUT_DIR, output_filename)
    new_image.save(output_path)
