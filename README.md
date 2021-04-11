[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)
[![Actions Status](https://github.com/brainglobe/slicereg/workflows/tests/badge.svg)](https://github.com/brainglobe/slicereg/actions)
[![Coverage Status](https://coveralls.io/repos/github/brainglobe/slicereg/badge.svg?branch=main)](https://coveralls.io/github/brainglobe/slicereg?branch=main)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=brainglobe_slicereg&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=brainglobe_slicereg)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/brainglobe/slicereg)

# slicereg
A 2D-3D histological brain slice registration application for mouse, rat, and zebrafish brains.

## Features

At the moment, only some very basic features are implemented:
  - Displays multi-channel OME-TIFF files onscreen.
  - Loads 25um and 100um resolution Allen Mouse Reference Atlas into a 3D visualizer
  - 2D slices can be translated and rotated in 3D space.

If you'd like to try it out, check the Installation section below.

## Next Steps

Next features are focused on manual registration in the GUI:
  - manual registration:
    - [x] Comparison widget between section and reference atlas
    - [x] Controls for full affine transforms
  - multi-slice handling:
    - [ ] Load multiple slices at once
    - [ ] Slice selection and multi-slice manipulation interface.
  - QuPath Visualization
    - [ ] Import QuPath files onto loaded slices for 3D visualization.
  - More control over visualization
    - [ ] View manipulation tools (channel selector, atlas transparency controls, qupath show/hide, etc)
    - [ ] CLim controls
   

  
## Installation

**NOTE!!!**
If you are using MacOS BigSur OpenGL will not work. We are still waiting on a solution from other developers on how to fix this

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

#### Troubleshooting
##### "Virtual environment already activated:"
To solve this you will need to use pip to install the dependencies:
```
poetry export -f requirements.txt --dev --without-hashes --output requirements.txt
pip install -r requirements.txt
```
##### Display issues
In some cases (e.g. using WSL), you might need to export the display.

  1. `export DISPLAY=:0`
  2. run Xming

##### Data download
In case DVC pull is not working
```
ERROR: failed to pull data from the cloud - Checkout failed for following targets:
```
  1. delete the folder **cache** in **.dvc**
  2. rerun `dvc pull`

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


## Contributors

Many thanks to:

  - Harald Reingruber: Organized Software Crafters to contribute to this project!