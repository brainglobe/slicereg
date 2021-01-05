# Repositories

This directory contains all the data loading/saving/persisting code. If the application needs a Section or Atlas (defined in the `domain` directory) 
from a file or service, these classes have methods that can get/save them.

*Note*: Currently this also includes file reading/writing. but future development may split that responsibility into its own
directory as more formats and people are involved.

## Design 

### Summary

Each repository is called by the Use Case functions, so it needs to have the interface that the use cases require 
(found in the `use_cases/base` directory).   This allows for multiple data backends to be supported and makes testing easier.

Currently, there are repositories for the `Atlas` and `Section` entities.

See the `main.py` file for how these are constructed and fed to the use cases.


### Philosophy

The repositories work as a backend-only.   This is the "Gateways" (i.e. Repository) and "DB" layer of the architecture.

![Clean Arch Diagram](https://miro.medium.com/max/875/1*EN-joV0Cr_gMn8aX06iHNQ.jpeg)

Each repo can store its data in whatever format it wants internally but must give domain objects (found in `domain` directory) 
back to the use cases.  This is great for performance/space optimization and supporting straightforward reimplementation of data handling.

 ### Guidelines
 
   - Repos currently are in a priviliged position to access the domain entities.  As such, they should call any of their methods or access their calculated properties, just contructing them and accessing their attributes.
  