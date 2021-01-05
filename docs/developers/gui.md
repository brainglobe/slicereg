# UI

This directory contains all the graphical interface code, implemented in PySide2 (Qt for Python) and Vispy.


## Design

### Summary
The Window/View works by sending commands to the UseCaseProvider methods, which in turn sends the data back to it via the Presenter.  
(e.g. Window -> UseCase -> Presenter(Window)).  Future development will likely split the Window/View/Presenter code further into Views/Controllers/Presenter/ViewModel
as the project grows and automated testing is added to speed development.See the `main.py` file to better-understand how those parts are connected.

### Philosophy

The gui works as a backend-only, relying on the use_cases directory to get the data it needs.

This is the "Presenters" and "UI" layer of the architecture:

![Clean Arch Diagram](https://miro.medium.com/max/875/1*EN-joV0Cr_gMn8aX06iHNQ.jpeg)


#### Use Case Provider 

To make it easier for the UI to access the use cases and instantiated, a Provider manager class is available.  This is 
essentially the [Facade Pattern](https://refactoring.guru/design-patterns/facade), used to simplify access to the classes:

![Facade Pattern Diagram](https://refactoring.guru/images/patterns/diagrams/facade/example.png) 

This facade is nice for now, but it may change in the future as the Controller and Presenter code becomes more seperate.

#### Controller / Presenter
  
The Window/View classes send commands to the use case functions (for example, requests for data, or changing a parameter), 
and the use case functions in turn send the data (if needed) via the Presenter class.  
This is done to make the classes simpler, keep the command code dependent on the use caess, and avoid circular dependencies:

![Presenter/Controller Diagram](https://miro.medium.com/max/283/1*zlbE57Ff2bXadvynsFmt_g.png)
 
To learn more, this blog article is a good first look: https://medium.com/@nishancw/clean-architecture-net-core-part-1-introduction-e70e1c49ef6

### Guidelines

  - Only the use_cases should be importing outside the package;
  - if new data are needed, new use cases should be added first, or existing use case presenters should be modified to supply more data.
    - Calculations should generally be pushed to the models; however, if the calculation is only related to the visualization and has no meaning outside the display and needs no extra data, then it's perfectly fine to do it in-place.  
    - In fact, as these display calculations increase, a new ViewModel class will be developed that localizes these calculations and makes them accessible to the Views and unit-testable  
  - The UI should not have access to any Domain objects; this is to increase flexibility to the domain, increase testability, and to reduce the number of processing- and persistence-related bugs
  
### Future development

  - This section will undergo the most change, as it's quite complex and will grow the most in early stages of the project.
  - As manual testing gets slower, a different design for this module will be selected to make automated testing easier. 