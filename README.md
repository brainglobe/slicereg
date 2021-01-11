[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)


# slicereg
A 2D-3D histological brain slice registration application for mouse brains.

## Features

At the moment, only some very basic features are implemented:
  - Displays multi-channel OME-TIFF files onscreen.
  - Loads 25um and 100um resolution Allen Mouse Reference Atlas into a 3D visualizer
  - 2D slices can be translated and rotated in 3D space.

If you'd like to try it out, check the Installation section below.

## Next Steps

Next steps are largely focused around deployment and development; this will ensure the tech stack is valid and make it easier to keep updating the project:
  - Get builds running for executable files on Windows, Mac, and Linux and confirm they work
  - Add continuous integration tooling to check builds, run static analysis tools, and test runner.
  - Auto-deployment and versioning.
  - Entry points for launching GUI from command line after pip install

Next features are focused on manual registration in the GUI:
  - manual registration:
    - Comparison widget between section and reference atlas
    - Controls for full affine transforms
  - multi-slice handling:
    - Load multiple slices at once
    - Slice selection and multi-slice manipulation interface.
  - QuPath Visualization
    - Import QuPath files onto loaded slices for 3D visualization.
  - More control over visualization
    - View manipulation tools (channel selector, atlas transparency controls, qupath show/hide, etc)
    - CLim controls
   

  
## Installation

### Using Python

#### Downloading the source code

Get a copy of the project onto your computer using git:

```
git clone https://github.com/brainglobe/slicereg
cd slicereg
```


#### Setting up the Project


This project uses [Poetry](https://python-poetry.org/) for installing dependencies; this is to make it easier for getting
the same versions of python libraries on everyones' computer and help manage virtual environments.  To get it, it can be pip-installed:

```
pip install poetry
``` 


To set up a virtual environment and install the dependencies (there are a lot of dependencies, this may take a couple minutes):

```
poetry install
```


*Note*: This project is python 3.8-only.  If you get an error that says that python 3.8 is not available, then one way you can get it is with conda, if you have it installed already:

```
conda create -n py38 python=3.8
conda activate py38
```

#### Running the Project

Run the program:

```
poetry run bg-slicereg
```



#### Downloading Test Data

Some test data can be made available for project developers.  
After you've been added to the access list, you can download it using DVC:

```
poetry run dvc pull
``` 

The first time you do this, there will be an authentication procedure.  
It will ask you to go to a Google Drive link and log in.  
Once you've logged in, copy-paste the authentication token from the browser into your terminal and press enter.  
The example data will appear in the project's data directory.

#### Documentation

Developer documentation is found in README files in the subdirectories.  
Open different folders to learn more about what their purpose is.


