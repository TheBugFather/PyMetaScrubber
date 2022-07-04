# PyMetaScrubber
![alt text](https://github.com/ngimb64/PyMetaScrubber/blob/main/PyMetaScrubber.png?raw=true)

## Prereqs
> This program runs on Windows and Linux, written in Python 3.9

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example:<br>
> python3 setup.py "venv name"

- Once virtual env is built move to the Scripts directory in the environment folder just created.
- In the Scripts directory, execute the "activate" script to activate the virtual environment.

## Purpose
PyMetaScrubber iterates through the contents of the DataScrubDock and attempts to scrub the file metadata.
If the metadata scrub fails, the file name is appending to list of failed items to be displayed upon completion.

## How to use
- Open shell or terminal and traverse to the program directory
- execute the program