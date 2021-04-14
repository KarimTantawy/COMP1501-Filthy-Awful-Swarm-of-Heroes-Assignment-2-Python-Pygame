![Image of Cover](https://github.com/KarimTantawy/COMP1501-Filthy-Awful-Swarm-of-Heroes-Assignment-2-Python-Pygame/blob/master/Filthy%2C%20Awful%20Swarm%20of%20Heroes/assets/Main_Menu.png)
# Filthy, Awful Swarm of Heroes
#### SCHOOL PROJECT - COMP 1501 - Winter 2019 Semester
  The specifications of this assignment required us to use Python and Utilize the Pygame library. This was a first year project and the 
structure/design of my code is reflective of such. I spent around 3-5 days on this assignment.

[![Video Thumbnail](https://www.youtube.com/watch?v=NccEsRrmjR0&ab_channel=KarimTantawy)

In Retrospect I would improve on the project in the following ways,
1. Would design project according to MVC Model
1. Remove every global variable(really bad practice)
1. Would create a 'character' superclass which all entities would inherit from
1. Would implement 'observer' design pattern to keep track of game state in level
   1. keep track of existing player character(s)
   1. Lots of unnecessary copy/pasting of code could have been avoided with the implementation of this pattern
1. Would create class template for enemies
   1. virtual attack() function, since attack functionality varies depending on the enemy
1. Any instance of Copy/Pasting of code would be removed and seperate function/class would be created for functionality
   E.g., user input could be made into a class 
1. Would implement sound effects/soundtrack
1. Would place a greater focus on optimization, avoiding/reducing unnecesary checks every update
   1. Would implement efficient data structures to keep track of entities, level, etc. such as ones learned in COMP 2402
1. Would implement better structure/design for Python code
1. Would break project down into separate logical files for readability and accessibility to be able to more easily add additional
features
