# Domain

This directory contains all the main algorithms, data validation, and data structures in the project.  Currently, these 
two structures are the **Atlas** (the 3D brain volume that is being used as a reference) and the **Section** 
(the 2D, multi-channel histological slice that's being registered).  

## Design

### Summary

This is the "Domain Model", meant to model the real-world aspect of the project (e.g. how slices are made in the cryostat, how experiments are organized, etc.).

![Cryostat](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Tissue_for_frozen_section_in_cryostat.JPG/220px-Tissue_for_frozen_section_in_cryostat.JPG)


### Philosophy


Because it's so important, the domain objects live in a self-contained part of the code; they don't depend on anything else.
This makes them easier to understand and test.  If you want to understand what the scope of this project is and what it's meant to do,
this directory is the best place to start.

This is the "Entities" part of the architecture, found in the center of the diagram:

![Clean Arch Diagram](https://miro.medium.com/max/875/1*EN-joV0Cr_gMn8aX06iHNQ.jpeg)

Ideally, only the Use Case functions can interact with them (to protect from developing leaky abstractions), but at this stage in the project the Repositories have been allowed to
import them for construction (with restrictions, see the repository README guidelines for details.)

### Guidelines

  - Also ideally, this code would be pure-python (no library dependencies), but for performance reasons Numpy has also been allowed.
  - Other libraries can be used for calculation, but should be in their own module (currently `utils.py`).  This is to make unit testing and swapping dependencies easier.  
