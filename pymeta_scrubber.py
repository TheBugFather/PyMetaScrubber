# pylint: disable=W0106,E0401
""" Built-in modules """
import os
import re
import sys
from pathlib import Path
from warnings import filterwarnings
# External modules #
from exif import Image
from pdfrw import PdfParseError, PdfReader, PdfWriter
from plum.exceptions import UnpackError


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
    except (AttributeError, OSError, UnpackError, ValueError):
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

    # If error occurs scrubbing pdf data #
    except (PdfParseError, UnpackError, ValueError):
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
    if not scrub_dir.exists():
        # Create the image scrubber dir #
        scrub_dir.mkdir(parents=True)
        print_err(f'Unable to run program because {scrub_dir.name} was missing,'
                 ' put data to be scrubbed in it and restart')
        sys.exit(2)

    print(r'''

-__ /\\           /\\,/\\,         ,          -_-/                   ,,    ,,                
  ||  \\         /| || ||         ||    _    (_ /                    ||    ||                
 /||__|| '\\/\\  || || ||   _-_  =||=  < \, (_ --_   _-_ ,._-_ \\ \\ ||/|, ||/|,  _-_  ,._-_ 
 \||__||  || ;'  ||=|= ||  || \\  ||   /-||   --_ ) ||    ||   || || || || || || || \\  ||   
  ||  |,  ||/   ~|| || ||  ||/    ||  (( ||  _/  )) ||    ||   || || || |' || |' ||/    ||   
_-||-_/   |/     |, \\,\\, \\,/   \\,  \/\\ (_-_-   \\,/  \\,  \\/\\ \\/   \\/   \\,/   \\,  
  ||     (      _-                                                                           
          -_-                                                                                 
    ''')
    print(f'Scrubbing images in {scrub_dir.name}:\n{"*" * (21 + (len(scrub_dir.name)))}\n')

    # If OS is Windows
    if os.name == 'nt':
        # Grab only the rightmost directory of path save result in other regex as anchor point #
        re_edge_path = re.search(r'[^\\]{1,255}$', str(scrub_dir))
        # Insert path edge regex match into regex to match any path past the edge anchor point #
        re_ext_path = re.compile(rf'(?<={re.escape(str(re_edge_path.group(0)))}\\).+$')
    # If OS is Linux #
    else:
        # Grab only the rightmost directory of path save result in other regex as anchor point #
        re_edge_path = re.search(r'[^/]{1,255}$', str(scrub_dir))
        # Insert path edge regex match into regex to match any path past the edge anchor point #
        re_ext_path = re.compile(rf'(?<={re.escape(str(re_edge_path.group(0)))}/).+$')

    # Recursively walk through the file system of the source path #
    for dir_path, _, file_names in os.walk(scrub_dir):
        # Attempt to match recursive path extending beyond base dir #
        match = re.search(re_ext_path, dir_path)
        # If match is successful #
        if match:
            # Set the match as path #
            recursive_path = Path(str(match.group(0)))
        else:
            recursive_path = None

        # Iterate through the files in current path #
        for file in file_names:
            # If the file is the dummy file for git tracking #
            if file == '.keep.txt':
                continue

            # If the path is in a recursive subdirectory #
            if not recursive_path:
                # Format file path for current iteration #
                curr_file = scrub_dir / file
            # If the path is not in a recursive subdirectory #
            else:
                # Format file path for current iteration #
                curr_file = scrub_dir / recursive_path / file

            # If the file is a PDF #
            if file.endswith('.pdf'):
                # If scrubbing the PDF metadata failed #
                if not pdf_scrub(str(curr_file)):
                    # Add file to failures list and loop #
                    failures.append(curr_file.name)
                    continue
            # If the file is a image #
            elif file.endswith(pic_ext):
                # If scrubbing the PDF metadata failed #
                if not pic_scrub(curr_file):
                    # Add file to failures list and loop #
                    failures.append(curr_file.name)
                    continue
            # If file is not a format that has metadata #
            else:
                continue

            print(f'Item  =>  {file}')

    # If there files that failed to be scrubbed #
    if failures:
        print(f'\n\nThe following items failed to have their metadata scrubbed:\n{"*" * 61}\n')
        [print(fail) for fail in failures]


if __name__ == '__main__':
    # Current working directory #
    cwd = Path.cwd()
    # Windows scrub dock directory #
    scrub_dir = cwd / 'DataScrubDock'

    RET = 0
    try:
        main()

    except Exception as ex:
        print_err(f'Unknown exception occurred: {ex}')
        RET = 1

    sys.exit(RET)
