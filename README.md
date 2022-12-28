# PyMetaScrubber
![alt text](https://github.com/ngimb64/PyMetaScrubber/blob/main/PyMetaScrubber.gif?raw=true)
![alt text](https://github.com/ngimb64/PyMetaScrubber/blob/main/PyMetaScrubber.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.85/10

## Prereqs
This program runs on Windows 10 and Debian-based Linux, written in Python 3.9 and updated to version 3.10.6

## Purpose
PyMetaScrubber iterates through the contents of the DataScrubDock and attempts to scrub the file metadata.
If the metadata scrub fails, the file name is appending to list of failed items to be displayed upon completion.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br>
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use
- Open shell or terminal and traverse to the program directory
- Ensure the setup script has been run and the virtual environment is activated
- Ensure exif files are in the DataScrubDock
- Execute the program

## Function Layout
-- pymeta_scrubber.py --
> pdf_scrub &nbsp;-&nbsp;  Scrubs the metadata from the passed in PDF file name.

> pic_scrub &nbsp;-&nbsp;  Scrubs the metadata from the passed in image file name.

> print_err &nbsp;-&nbsp; Displays passed in error message via stderr.

> main &nbsp;-&nbsp; Checks for scrub directory to load images and scrub metadata. Failures are 
> appended to list to be displayed when the program finishes.

## Exit Codes
> 0 - Successful operation (__main__)
> 1 - Unexpected exception occurred (__main__)
> 2 - ScrubDirectory dock for data to be scrubbed does not exist (main)