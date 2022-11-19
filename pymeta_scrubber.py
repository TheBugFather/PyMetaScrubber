# pylint: disable=W0106
""" Built-in modules """
import os
import sys
from warnings import filterwarnings
# External modules #
from exif import Image
from pdfrw import PdfParseError, PdfReader, PdfWriter


# Current working directory #
cwd = os.getcwd()
# Windows scrub dock directory #
if os.name == 'nt':
    SCRUB_DIR = f'{cwd}\\DataScrubDock\\'
# Linux scrub dock directory $
else:
    SCRUB_DIR = f'{cwd}/DataScrubDock/'


def pdf_scrub(pdf_file) -> bool:
    """
    Scrubs the metadata from the passed in PDF file name.

    :param pdf_file:  The PDF file whose metadata is to be scrubbed.
    :return:  Boolean True/False on success/fail.
    """
    try:
        # Read the PDF file data #
        pdf = PdfReader(f'{SCRUB_DIR}{pdf_file}')

        # Iterate through PDF file metadata and delete it #
        for metadata in pdf.Info:
            del pdf.Info[metadata]

        # Re-write the scrubbed PDF data back to file #
        PdfWriter(f'{SCRUB_DIR}{pdf_file}', trailer=pdf).write()

    except PdfParseError as pdf_err:
        # Print error and return false #
        print_err(f'Error occurred attempting to scrub PDF metadata: {pdf_err}')
        return False

    return True

def pic_scrub(img_file) -> bool:
    """
    Scrubs the metadata from the passed in image file name.

    :param img_file:  The image file whose metadata is to be deleted.
    :return:  Boolean True/False on success/fail.
    """
    try:
        # Read the data of the file to be scrubbed #
        with open(f'{SCRUB_DIR}{img_file.name}', 'rb') as in_file:
            meta_file = Image(in_file)

        # Delete all metadata #
        meta_file.delete_all()

        # Overwrite file with scrubbed data #
        with open(f'{SCRUB_DIR}{img_file.name}', 'wb') as out_file:
            out_file.write(meta_file.get_file())

    # If file IO error occurs #
    except (AttributeError, IOError, Warning) as file_err:
        # Print error and return false #
        print_err(f'Error occurred attempting to scrub image metadata: {file_err}')
        return False

    # If obscure keys were unable to be scrubbed #
    except KeyError:
        pass

    return True


def print_err(msg: str):
    """
    Displays passed in error message via stderr.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


def main():
    """
    Checks for scrub directory to load images and scrub metadata. Failures are appended to list to \
    be displayed when the program finishes.

    :return:  Nothing
    """
    # List for files that fail meta-scrubbing #
    failures = []
    # Tuple grouping of picture file extensions #
    pic_ext = ('.png', '.jpg', '.jpeg', '.bmp')
    # Ignore benign exif warnings #
    filterwarnings('ignore')

    # If the image scrubber dir does not exist #
    if not os.path.isdir(SCRUB_DIR):
        # Create the image scrubber dir #
        os.mkdir(SCRUB_DIR)
        print_err(f'Unable to run program because {SCRUB_DIR} was missing,'
                 ' put data to be scrubbed in it and restart')
        sys.exit(1)

    print(f'\nScrubbing images in {SCRUB_DIR}:\n{"*" * (21 + (len(SCRUB_DIR)))}\n')

    # Iterate through the files in the images scrubber dir #
    for file in os.scandir(SCRUB_DIR):
        # If the current item is dir or the dummy file for git tracking #
        if os.path.isdir(f'{SCRUB_DIR}{file.name}') or file.name == '.keep.txt':
            # Skip to the next item #
            continue

        # If the file is a PDF #
        if file.name.endswith('.pdf'):
            # If scrubbing the PDF metadata failed #
            if not pdf_scrub(file.name):
                continue
        # If the file is a image #
        elif file.name.endswith(pic_ext):
            # If scrubbing the PDF metadata failed #
            if not pic_scrub(file.name):
                continue
        # If file is not a format that has metadata #
        else:
            continue

        print(f'Item  =>  {file.name}')

    # If there files that failed to be scrubbed #
    if failures:
        print(f'\n\nThe following items failed to have their metadata scrubbed:\n{"*" * 61}\n')
        [print(fail) for fail in failures]


if __name__ == '__main__':
    main()
