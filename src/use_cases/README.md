# Use Cases

This directory contains all the meaningful actions (called "Use Cases") that a user can do in the application, each action getting its own file to make it 
easier to find.  A use case tends to be a straightforward workflow (e.g. get some data, then calculate some value, then show it onscreen).

If you were writing an academic paper about this project, each Use Case would be a sentence in the paper (e.g. Users can Move Sections to a given coordinate and orientation in the reference atlas). 

## Design

### Summary 

To make it simpler to describe the workflow and keep it focused on the big-picture features, this code doesn't directly depend on any
libraries; instead, it indirectly uses them via base classes it specifies (and other code needs to implement).  

### Philosophy

#### Architecture

This is the "Entities" part of the architecture, found in the center of the diagram:

![Clean Arch Diagram](https://miro.medium.com/max/875/1*EN-joV0Cr_gMn8aX06iHNQ.jpeg) 

Doing it this way gives the Use Cases a lot of control over how things are done without needing to manage a lot of computational details. 
It also makes it easier to add more Use Cases without breaking old ones (a "vertical" architecture).


#### Provider 

To make it easier for the UI to access the use cases and instantiated, a Provider manager class is available.  This is 
essentially the [Facade Pattern](https://refactoring.guru/design-patterns/facade), used to simplify access to the classes:

![Facade Pattern Diagram](https://refactoring.guru/images/patterns/diagrams/facade/example.png) 

This facade is nice for now, but it may change in the future if use cases become more inter-dependent (but hopefully not).

#### Errors

All decisions should really be made by the Use Case, and that includes what do do if things go wrong.  Although it's not
totally possible to do in Python, use cases development should strive to never allow exceptions to propogate outside them;
as such, the Presenters usually have a `show_error(msg: str)` function that allows them to send feedback to the user without
exposing the Python issues to them.
 

### Guidelines

  - Each Use Case should define its own BasePresenter.  
    - This may seems like overkill, but it makes testing and future development way easier.
    - In practice, this means that every new use case will also mean new presenter code in the UI, new commands in the Window, and new view code for seeing the output.
    - If you make the BasePresenter method names unique, the UI Presenter can just inherit from all the BasePresenters. In practice, this is pretty nice. 
  - Use Cases currently can share Repositories.
    - It should only reference repositories it actually uses, though.  This is for ease of testing.
    - If for some reason data handling gets way more complex (not likely), then each use case will define its own BaseRepo as well.
  - Use Cases should only use Domain entity Class methods in their calculation work; all real calculations should be done in the domain layer.
    - This is for ease of unit testing.
  - Use Cases will have to be tested.  This will involve a good bit of Mocking of the Repo and Presenters, so keep them as simple and straightforward as possible.
  
