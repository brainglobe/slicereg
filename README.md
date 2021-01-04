[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)


# slicereg
A 2D-3D histological brain slice registration application for mouse brains.


## Development and Testing

### Setting up the Project

Get the source code onto your computer using git:

```
git clone https://github.com/brainglobe/slicereg
```

Use conda to create a virtual environment with all the necessary dependencies for running the application:

```
cd slicereg
conda env create -f environment.yml
conda activate slicereg 
```

Install additional optional dependencies (just for extra things, like getting test data, running tests, creating build artifacts, docs, etc):

```
conda activate slicereg
pip install -f dev_requirements.txt
``` 


### Running the Project

Run the program:

```
conda activate slicereg
python main.py
```

### Downloading Test Data

Some test data can be made available for project developers.  
After you've been added to the access list, you can download it using DVC:

```
dvc pull
``` 

The first time you do this, there will be an authentication procedure.  
It will ask you to go to a Google Drive link and log in.  
Once you've logged in, copy-paste the authentication token from the browser into your terminal and press enter.  
The example data will appear in the project's data directory.

 