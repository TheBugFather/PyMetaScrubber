# Built-in modules #
import os
import sys
from warnings import filterwarnings

# External modules #
from exif import Image

# Current working directory #
cwd = os.getcwd()
# Windows scrub dock directory $
if os.name == 'nt':
    IMAGE_DIR = f'{cwd}\\DataScrubDock\\'
# Linux scrub dock directory $
else:
    IMAGE_DIR = f'{cwd}/DataScrubDock/'


"""
########################################################################################################################
Name:       PrintErr
Purpose:    Displays passed in error message via stderr.
Parameters: The error message to be displayed via stderr.
Returns:    Nothing
########################################################################################################################
"""
def PrintErr(msg: str):
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


"""
########################################################################################################################
Name:       main
Purpose:    Checks for scrub directory to load images and scrub metadata. Failures are appended to list to be \
            displayed when the program finishes. 
Parameters: Nothing
Returns:    Nothing
########################################################################################################################
"""
def main():
    # List for files that fail meta-scrubbing #
    failures = []
    # Ignore benign exif warnings #
    filterwarnings('ignore')

    # If the image scrubber dir does not exist #
    if not os.path.isdir(IMAGE_DIR):
        # Create the image scrubber dir #
        os.mkdir(IMAGE_DIR)
        PrintErr(f'Unable to run program because {IMAGE_DIR} was missing,'
                 ' put data to be scrubbed in it and restart')
        sys.exit(1)

    print(f'\nScrubbing images in {IMAGE_DIR}:\n{"*" * (21 + (len(IMAGE_DIR)))}\n')

    # Iterate through the files in the images scrubber dir #
    for image_file in os.scandir(IMAGE_DIR):
        # If the current item is dir or the dummy file for git tracking #
        if os.path.isdir(f'{IMAGE_DIR}{image_file.name}') or image_file.name == '.keep.txt':
            # Skip to the next item #
            continue

        try:
            # Read the data of the file to be scrubbed #
            with open(f'{IMAGE_DIR}{image_file.name}', 'rb') as in_file:
                meta_file = Image(in_file)

            # Delete all metadata #
            meta_file.delete_all()

            # Overwrite file with scrubbed data #
            with open(f'{IMAGE_DIR}{image_file.name}', 'wb') as out_file:
                out_file.write(meta_file.get_file())

            print(f'Item  =>  {image_file.name}')

        # If file IO error occurs #
        except (AttributeError, KeyError, IOError, Warning):
            # If error suggests failed scrub #
            if not KeyError:
                # Append failed item to list #
                failures.append(image_file.name)

    # If there files that failed to be scrubbed #
    if failures:
        print(f'\n\nThe following items failed to have their metadata scrubbed:\n{"*" * 61}\n')
        [print(fail) for fail in failures]


if __name__ == '__main__':
    main()