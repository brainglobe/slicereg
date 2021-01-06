
# Code Organization

## What Code is Where?

  - **Core**: This is where the meat of the project is; all the scientific work and feature descriptions are here.  
    - Each of the directories is organized around a core concept involved in slice registration (the focus of this project). This means that the number/name of the directories may increase as better-fitting concepts are found, which is a natural aspect of research and development. 
    - **models.py** : Contains the The main data structures, scientific concepts, and algorithms.  
      - This is the most important file, and reading it should give you a good idea of what the directory does.
    - **xxx_xxx.py** : These are the workflows that the application can perform. 
      - Each pipeline is self-contained in its own procedure (it returns nothing) and has descriptions of what it needs to perform its work.
      - As a result, other applications will do the actual supplying and constructing of the data it needs. This code is meant to be very abstract and keep to the big-picture view.
    - **base.py**: Contains abstract classes ("base" classes) that other modules in the directory might use.
    
  - **GUI**: This contains the code for the graphical interface.  All the windows, controllers, buttons, visualizations, etc.
    - The gui code doesn't have access to the models, it just gets whatever data the Presenter (defined by the workflow) supplies.  So no need to understand all the models before understanding the gui.
    - The use cases the gui has access to are defined in the **workflows.py** module.  When new use cases are created, they can be wired up to the gui by adding them to the WorkflowProvider in this module.
      - As a result, new workflows can be created without accidentally breaking the gui in the process. 
  
  - **Repos**: This contains code for memory management of the different models. If a workflow needs to get an Atlas, for example, it can ask for one from the bg_atlas repo.
    - Each repo has methods that are defined by the base repo classes in the use case code in **core**. That is; the use cases say what they need, and the repos figure out how to supply it. 
    - This may seem a bit convoluted for something as simple as getting a variable, but it provides a flexible way for controlling how/where data is stored.  If read/write optimizations are necessary or different libraries swapped out, it can be done safely here without breaking the other code.
    
  - **Serializers**: Contains file read/write code for the models for different file formats.
  
  
## I want to <x>, where do I look?

### I want to add a button or change the way existing data is shown onscreen.

Great!  Just go to the gui directory.  The buttons for the main window are in **window.py**, and the other widgets are in their own **xxx_view.py** modules.  These classes are pretty self-contained, so making changes to any existing methods, or adding new ones, should be straightforward.

### I want to add a new way to load data from file.  
  
Got a different source of reference atlas, or a different file format for your slices?  Great!  You'll need a new Serializer.
Just add a new file to the serializers directory and look at the **ome_tiff.py** example for how to get started.

### I want to expose more data from the models to the gui.

For this, you'll need to identify which workflow should present that data to the gui, and add it to its associated presenter.  
Right now this requires a few steps, but as the project grows we'll refactor a bit to make it easier to do and have more places for testing.  Here's what to do at the moment:

  1. Add the code in the gui for displaying the data as a new method in the view.
  2. Edit the Presenter (in **gui/presenter.py**) to call your new method for the workflows that are relevant.  
    - Try it out with some dummy data to make sure it appears onscreen the way you like.  This is a great chance to toy around with things and get it how you want. 
  3. Add an argument to the both the Presenter method and the associated BasePresenter in the workflows.  This way the Workflow can supply the data to the presenter.
  4. Modify the Workflow function (under **\_\_call(self)\_\_**) to get the data from the models and give it to the presenter
    - Run it!  It should work!
    
### I want to add some scientific code.

Great!  If it's a new property of an existing model, go ahead and add it!  It it's a change to how an existing property/method is calculated, make the change!

If it's a name change to something that's much more familiar, go ahead and change it, and check the use cases for the name change as well (the **xxx_xxx.py** files)!

If it's an entirely new model, then it might deserve its own directory or just be an additional model next to something else closely-related.  Go ahead and add it, then schedule a discussion about what the new model represents; once we all understand it, we can build workflows around it. 

### I want to add automated tests to the code.

Great!  Since this project is currently in a pre-alpha state, we're relying on static type analysis (mypy) to do some automated testing, but as the project becomes actually useful (i.e. when it starts exporting data), we'll use Pytest to check the models.  This progression is for keeping things flexible during the early design stage. 
   
### References

  - Screaming Architectures and why they are valuable: https://levelup.gitconnected.com/what-is-screaming-architecture-f7c327af9bb2
  - Domain-Driven Design: https://airbrake.io/blog/software-design/domain-driven-design
  - Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
  