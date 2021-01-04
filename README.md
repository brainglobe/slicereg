[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)


# slicereg
A 2D-3D histological brain slice registration application for mouse brains.


## Development and Testing

### Downloading the source code

Get a copy of the project onto your computer using git:

```
git clone https://github.com/brainglobe/slicereg
cd slicereg
```


### Setting up the Project


This project uses [Poetry](https://python-poetry.org/) for installing dependencies; this is to make it easier for getting
the same versions of python libraries on everyones' computer and help manage virtual environments.  To get it, it can be pip-installed:

```
pip install poetry
``` 


To set up a virtual environment and install the dependencies (there are a lot of dependencies, this may take a couple minutes):

```
poetry install
```

### Running the Project

Run the program:

```
poetry run python main.py
```

### Downloading Test Data

Some test data can be made available for project developers.  
After you've been added to the access list, you can download it using DVC:

```
poetry run dvc pull
``` 

The first time you do this, there will be an authentication procedure.  
It will ask you to go to a Google Drive link and log in.  
Once you've logged in, copy-paste the authentication token from the browser into your terminal and press enter.  
The example data will appear in the project's data directory.

 