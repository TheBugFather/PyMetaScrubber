# pylint: disable=W0106,E0401
""" Built-in modules """
import os
import sys
from pathlib import Path
from warnings import filterwarnings
# External modules #
from exif import Image
from pdfrw import PdfParseError, PdfReader, PdfWriter


# Current working directory #
cwd = Path.cwd()
# Windows scrub dock directory #
SCRUB_DIR = cwd / 'DataScrubDock'


def pic_scrub(img_file: Path) -> bool:
    """
    Scrubs the metadata from the passed in image file name.

    :param img_file:  The image file whose metadata is to be deleted.
    :return:  Boolean True/False on success/fail.
    """
    try:
        # Read the data of the file to be scrubbed #
        with img_file.open('rb') as in_file:
            meta_file = Image(in_file)

        # Delete all metadata #
        meta_file.delete_all()

        # Overwrite file with scrubbed data #
        with img_file.open('wb') as out_file:
            out_file.write(meta_file.get_file())

    # If error occurs during file or metadata scrubbing operation #
    except (AttributeError, IOError) as file_err:
        # Print error and return false #
        print_err(f'Error occurred attempting to scrub image metadata: {file_err}')
        return False

    # If obscure keys were unable to be scrubbed #
    except KeyError:
        pass

    return True


def pdf_scrub(pdf_path: str) -> bool:
    """
    Scrubs the metadata from the passed in PDF file name.

    :param pdf_path:  The PDF file whose metadata is to be scrubbed.
    :return:  Boolean True/False on success/fail.
    """
    try:
        # Read the PDF file data #
        pdf = PdfReader(pdf_path)

        # Iterate through PDF file metadata and delete it #
        for metadata in pdf.Info:
            del pdf.Info[metadata]

        # Re-write the scrubbed PDF data back to file #
        PdfWriter(pdf_path, trailer=pdf).write()

    except PdfParseError as pdf_err:
        # Print error and return false #
        print_err(f'Error occurred attempting to scrub PDF metadata: {pdf_err}')
        return False

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
    if not SCRUB_DIR.exists():
        # Create the image scrubber dir #
        SCRUB_DIR.mkdir(parents=True)
        print_err(f'Unable to run program because {SCRUB_DIR.name} was missing,'
                 ' put data to be scrubbed in it and restart')
        sys.exit(2)

    print(f'\nScrubbing images in {SCRUB_DIR.name}:\n{"*" * (21 + (len(SCRUB_DIR.name)))}\n')

    # Iterate through the files in the images scrubber dir #
    for file in os.scandir(SCRUB_DIR):
        # Format file path for current iteration #
        curr_file = SCRUB_DIR / file.name

        # If the current item is dir or the dummy file for git tracking #
        if curr_file.is_dir() or file.name == '.keep.txt':
            # Skip to the next item #
            continue

        # If the file is a PDF #
        if file.name.endswith('.pdf'):
            # If scrubbing the PDF metadata failed #
            if not pdf_scrub(str(curr_file)):
                # Add file to failures list and loop #
                failures.append(curr_file.name)
                continue
        # If the file is a image #
        elif file.name.endswith(pic_ext):
            # If scrubbing the PDF metadata failed #
            if not pic_scrub(curr_file):
                # Add file to failures list and loop #
                failures.append(curr_file.name)
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
    RET = 0
    try:
        main()

    except Exception as ex:
        print_err(f'Unknown exception occurred: {ex}')
        RET = 1

    sys.exit(RET)
