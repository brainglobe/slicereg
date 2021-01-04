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

  
The Window/View classes send commands to the use case functions (for example, requests for data, or changing a parameter), 
and the use case functions in turn send the data (if needed) via the Presenter class.  
This is done to make the classes simpler, keep the command code dependent on the use caess, and avoid circular dependencies:

![Presenter/Controller Diagram](https://miro.medium.com/max/283/1*zlbE57Ff2bXadvynsFmt_g.png)
 
To learn more, this blog article is a good first look: https://medium.com/@nishancw/clean-architecture-net-core-part-1-introduction-e70e1c49ef6
