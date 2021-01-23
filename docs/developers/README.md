
# Code Organization

## What Code is Where?

  - **models**: This is where the meat of the project is; all the calculations and scientific work are here.
    
  - **commands**: 
    - **xxx_xxx.py** : These are the commands that the application can perform. 
      - Each pipeline is self-contained in its own procedure (it returns nothing) and has descriptions of what it needs to perform its work.
      - As a result, other applications will do the actual supplying and constructing of the data it needs. This code is meant to be very abstract and keep to the big-picture view.
    - **base.py**: Contains abstract classes ("base" classes) that other modules in the directory might use.
    
  - **gui**: This contains the code for the graphical interface.  All the windows, controllers, buttons, visualizations, etc.
    - The gui code doesn't have access to the models, it just gets whatever data the command supplies when its Signal is called.  So no need to understand all the models before understanding the gui.
    - As a result, new commands can be created without accidentally breaking the gui in the process. 
  
  - **repos**: This contains code for memory management of the different models. If a command needs to get an Atlas, for example, it can ask for one from the bg_atlas repo.
    - Each repo has methods that are defined by the base repo classes in the use case code in **core**. That is; the use cases say what they need, and the repos figure out how to supply it. 
    - This may seem a bit convoluted for something as simple as getting a variable, but because no globals are created, it provides a flexible way for controlling how/where data is stored.  
    
  - **io**: Contains file read/write code for the models for different file formats.
  
  
## I want to <x>, where do I look?

### I want to add a button or change the way existing data is shown onscreen.

Great!  Just go to the gui directory.  The buttons for the main window are in `window.py`, and the other widgets are in their own `xxx_view.py` modules.  These classes are pretty self-contained, so making changes to any existing methods, or adding new ones, should be straightforward.

If you want some method to be called whenever a particular Command event happens, just connect it up in the `main.py` (you'll see examples of how to do it there.)

### I want to add a new way to load data from file.  
  
Got a different source of reference atlas, or a different file format for your slices?  Great!  That'll be in `io`.
Just look at the **ome_tiff.py** example for how to get started.

### I want to expose more data from the models to the gui.

For this, you'll need to identify which command should present that data to the gui, and add it to its associated presenter.  
Right now this requires a few steps, but as the project grows we'll refactor a bit to make it easier to do and have more places for testing.  Here's what to do at the moment:

  1. Add the code in the gui for displaying the data as a new method in the view.
    - Try it out with some dummy data to make sure it appears onscreen the way you like.  This is a great chance to toy around with things and get it how you want. 
  2. Modify the Command function (under **\_\_call(self)\_\_**) to get the data from the models and give it to the presenter
    - Run it!  It should work!
    
### I want to add some scientific code.

Great!  If it's a new property of an existing model, go ahead and add it!  It it's a change to how an existing property/method is calculated, make the change!  So long as you add tests for the new code, it's very welcome.

If it's a name change to something that's much more familiar, go ahead and change it, and check the use cases for the name change as well (the **xxx_xxx.py** files)!

If it's an entirely new model, then it might deserve its own directory or just be an additional model next to something else closely-related.  Go ahead and add it, then schedule a discussion about what the new model represents; once we all understand it, we can build commands around it. 

### I want to add automated tests to the code.

Great!  Since this project is currently in a pre-alpha state, we're relying on static type analysis (mypy) to do some automated testing, but as the project becomes actually useful (i.e. when it starts exporting data), we'll use Pytest to check the models.  This progression is for keeping things flexible during the early design stage. 
  
  
## Code Design Philosophy

This codebase is largely built on the "Clean Architecture", with influences from the "Vertical Slice Architecture", "Hexagonal Architecture", and "Domain Driven Design".
The core idea of these architectures is about controlling the dependencies of different modules, with dependencies all pointing toward the core domain model of the code
and having isolation between the various devices that the application uses (graphics, user events, database, filesystem, etc) and the core calculations.  This involves a lot
of using the "Dependency Inversion Principle" to inject those tools into the call stack.  

![Clean Arch Diagram](https://miro.medium.com/max/875/1*EN-joV0Cr_gMn8aX06iHNQ.jpeg)

Layered architectures can be quite overwhelming to work with, and to simplifiy that organization, each user actions is self-contained.  These "Vertical Slices" should help us stay flexible.
Using Behavioral-Driven-Design, each command can also be tested individually and use just the portion of code it needs to. 

![Vertical Slice Architecture](https://1.bp.blogspot.com/-olkFpMS9FN8/W07kxIzfoTI/AAAAAAAAB-w/q2OMoo85kPwT7Buvbf4ErLw7BmTuosL5wCLcBGAs/s1600/vertical%2Bslices%2Bjimmy%2Bbogard.png)

The Python scientific ecosystem is contantly improving.  By isolating the infrastructure from the rest of the code, we will be free to swap them out as new opportunities come up.  
By letting these systems plug into a highly-tested set of core code, the project should be maintainable for many years to come.  

### Dos and Do Nots
  - **Do** write your tests before writing your implementation code.  
    - New Commands: Feature files first, then Command Tests, then the Command implementations.
    - New Models / Model methods: Unit tests first, cycling between progressively more-general unit tests and next-step implementations.
    - New GUI interaction: No test required at present, because graphics are hard to test.
  - **Do** make code improvements inside methods as you find them. 
  - **Do** use type annotations everywhere in your code.
  - **Do** pair and mob program with the other developers in the code
  - **Do Not** do any math in the gui, repo, or io code.  Gui code should *only* transfer existing data to the screen, repos should only store/access data, io should only interact with the filesystem.
  - **Do Not** import models into the `main.py` or `gui` modules.  `repo` and `io` may pass models, though. 
  - **Do Not** send models from the Commands to whoever is calling them. The external layers shouldn't have any access!
  - **Do Not** create a Command without first writing the test for it.  It's not easy to write a Command that is easy to test; writing the test first will push you to make solid design decisions and earlier in the process. 
  - **Do Not** make the core model code depend on any objects for third-party python libraries.  We want the inner layers of the code to be very stable!  
  
### References

  - Screaming Architectures and why they are valuable: https://levelup.gitconnected.com/what-is-screaming-architecture-f7c327af9bb2
  - Domain-Driven Design: https://airbrake.io/blog/software-design/domain-driven-design
  - Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
  - Vertical Slice Architecture: https://www.youtube.com/watch?v=SUiWfhAhgQw&feature=emb_logo
  
  