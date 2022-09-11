# NezertorcheaT Console Engine

## Welcome to the NezertorcheaT Console Engine documentation!

And let's start with the fact that in order to work, you need Python installed on your computer, and the downloaded repository
the project itself, in a separate folder.

To try out a test project, run the main.py file.

The map editor is opened by running the redactor.py file.
The fields "**Height**" and "**Width**" are responsible for the size of the playing field.
By writing numbers greater than 1 there and pressing "**Set Grid Size**" you will save these values ​​in the globalSettings.json file.
The "**Save Map**" button will save the map to the globalMap.json file.
By clicking on the cells, the menu for creating an object will open, but first you need to enter the name of one of the licking classes in the folder
Scripts.

Next, there will be a property editor window, it must contain properties: "**name**", "**spawnposx**", "**spawnposy**"
, "**symbol**", "**parent**"
and "**collide**". You can also add these properties in scripts yourself.

The "**name**" property is responsible for the name, and if the entered name exists, the object with that name will be overwritten.
The "**spawnposx**" property is responsible for the initial local position of the object along the X axis.
The "**spawnposy**" property is responsible for the initial local position of the object along the Y axis.
The "**symbol**" property is responsible for the symbol of the object in the world.
The "**collide**" property is responsible for the possibility of collision with other objects.
The "**parent**" property is responsible for the parent of the object and takes the name of the object
The "**Save**" button is responsible for saving the object on the map.

This is all the functionality of the map editor for now.

## Now the fun part! Your scripts!

In the Scripts folder, you can create your own files, in the likeness of the existing ones. Your script should look like this:

```
#<imports>
from NTEngineClasses import *

class Name(Behavior):
    spawnposx = 0
    spawnposy=0
    symbol = '@'
    collide = True

    def start(self):
        #<code>
    
    def update(self, a):
        #<code>
        if not self.isInstantiated:
            #<ui_code>
    def onCollide(self, collider: Transform):
        pass
    def lateUpdate(self, a):
        Drawer().drawSymb(a, "8", Vec3(1, 1))
        
```

### Explanation of methods:

1. NTETime:
    - **getTime()** - returns the current frame
2. ObjList:
    - **getObj(i: int)** - get an object
    - **getObjs()** - get all objects
3.globalSettings:
    - **settings** - all fields from the globalSettings.json file
    - **objMap** - map from globalMap.json file
4.NTEngineClasses:
    - **object ui** - representation of the UI class
    - **UI class**:
        - **add(text, createNewLine: bool) -> int** - adds a new line to the array of strings, field "createNewLine"
          is responsible for creating a new line at the end, returns the position of the new line in the array
        - **clearSpace(i: int, createNewLine: bool)** - clears the line with number "i", field "createNewLine" is responsible for
          creating a newline at the end
        - **changeSpace(i: int, text='', createNewLine=True)** - changes the properties of the i-th line to new ones
    - Vec3 class:
        - **Vec3.dev_by_float(a, n=1)** - divides the vector "a" by the number "n"
        - **Vec3.mult_by_float(a, n=0)** - multiplies the vector "a" by the number "n"
        - **Vec3.sum(a, b)** - sum of vectors "a" and "b"
        - **Vec3.substr(a, b)** - subtracts vector "b" from vector "a"
        - **Vec3.mult(a, b)** - multiplies the components of the vector "a" by the components of the vector "b"
        - **Vec3.div(a, b)** - divides the components of the vector "a" into the components of the vector "b"
        - **Vec3.distance(v1, v2)** - distance between vectors "v1" and "v2"
        - **Vec3.dot(a, b)** - Dot product of vectors "a" and "b"
        - **Vec3.reflect(rd, n)**
        - **length()** - vector length
        - **abs()**
        - **normal()**
        - **sign()**
    - **Transform class**:
        - **local_position: Vec3** - local position of the object
        - **collide: bool** - collision calculation
        - **beh: Behavior** - link to behavior
        - **moweDir(Dir: Vec3)** - add "Dir" vector to position, adjusted for physics
        - **setLocalPosition(V: Vec3)** - move local position to "V" verctor, adjusted for physics
        - **getPosition()** - get the global position of the object in the world
    - **obj class**:
        - **tr: Transform** - Transform class
        - **symb: str** - displayed symbol
    - **Drawer class**:
        - **drawSymb(a, symb: str, pos: Vec3)** - used to draw symbol "symb" at position "pos", works
          only in "lateUpdate"
        - **clearSymb(a, pos: Vec3)** - used to clear symbol at position "pos", only works in "
          lateUpdate"
    - **Behavior class**:
        - **isInstantiated: bool** - determines if the object was created using the instantiate() method
        - **update(self, a)** - called every world update
        - **start(self)** - called at the very beginning
        - **onCollide(self, collider: Transform)** - called when collidecontact with an object
        - **lateUpdate(self, a):** - called after "update"
        - **passSteps(frames: int)** - used to completely stop the object for "frames" ticks
        - **passSeconds(secs: float)** - used to completely stop the object for "secs" seconds
        - **instantiate(beh, Pos: Vec3) -> int** - used to create objects at position "pos" with behavior "beh"
          , "beh" must be set to a type inherited from Behavior, returns the position of the created object in the array
          objects, example code: ```instantiate(Scripts.FireBall.FireBall, self.gameobject.tr.position)```
    - **clamp(num, min_value, max_value)** - the simplest variable constraint
    - **findNearObjByPos(V: Vec3, f: float, b=[])** - returns objects in radius "f" to position "V", excluding all
      objects from the list "b", there you need to put objects of a type that is inherited from Behavior
    - **destroy(beh)** - deletes the object "beh" from the world

# That's all! Thanks for reading!
