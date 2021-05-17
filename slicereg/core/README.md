


## Code Questions & Learning Resources

### Why Section.create()?  Why not Section.\_\_init\_\_(), so we can just call Section()?

This project makes heavy use of static typing and static type analysis to check for potential bugs in the code; 
this puts a specific requirement on every class:  
*"Every class must declare all of its attributes before construction."*

Python dataclasses make that part easy: instance attribute goes under the classname,
along with its type, the same as with every other method and property in the class.  
It even lets us declare default values to work with for each attribute, making it simpler to construct the class 
from partial information.

But what if the default value of one attribute should be based on another attribute?  Well, this can get complicated.
One solution is to create an alternate constructor function that handles that validation process; these are often
created as **@classmethods**, since they are meant to be run without have an instance of the class on-hand.
The nice thing about this approach is that it keeps the attribute types simple, doesn't add any validation code to be
managed during the life of the object, and simply adds complexity during the construction moment. 

This approach follows the general rule, **"Don't do any work in your constructors."**.  It has many benefits, and is a good policy in general for working with classes.

#### Resources

  - http://misko.hevery.com/code-reviewers-guide/flaw-constructor-does-real-work/