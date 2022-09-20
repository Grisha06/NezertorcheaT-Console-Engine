# NezertorcheaT Console Engine

## Welcome to the NezertorcheaT Console Engine documentation!

To try out a test project, run the main.py file.

The map editor is represented by a list of json files in the Maps folder.
The first field is the name of the map.
Further there are descriptions of game objects, and more specifically their names.
Inside the objects are the "**startPos**" and "**components**" fields.
The first is the representation of the starting position as a vector.
The second is the list of components.
It can lick any objects whose types are inherited from the "**Component**" class.
And it can lick the properties of these objects.

## Now the fun part! Your scripts!

In the Scripts folder, you can create your own files, in the likeness of the existing ones. Your script should look like this:

```
#<imports>
from NTEngineClasses import *

class Name(Behavior):
    def start(self):
        #<code>
    
    def update(self, a):
        #<code>

    def onCollide(self, collider: Transform):
        pass

    def onDraw(self, a):
        #<ui_code>
        #<draw_code>: Drawer().drawSymb(a, "8", Vec3(1, 1))
        
```

### Explanation of methods:

1. NTE Time:
    - **getTime()** - returns the current frame
2. ObjList:
    - **getObj(i: int)** - get an object
    - **getObjs()** - get all objects
    - **getObjByName(name: str)** - get object with name "name"
3.globalSettings:
    - **settings** - all fields from the globalSettings.json file
    - **objMaps** - map from Maps folder
4. Drawer:
    - **drawSymb(a, symb: str, pos: Vec3)** - draws symbol "symb" at position "pos" on matrix "a"
    - **drawSymbImage(a, img: str, pos: Vec3)** - draws a list of symbols stored in the TextImages folder named "img"
      at position "pos" on matrix "a"
5.NTEmapManager:
    - **loadLevel(mapname: str = "globalMap")** - loads the map stored in the Maps folder with the name "mapname"
    - **stopMainLoop(func)** - stops the main loop by throwing an error, but before that, executes the function "func"
6.NTEngineClasses:
    - **object ui** - representation of the UI class
    - **camera object** - representation of the Camera class
    - **UI class**:
        - **add(text, createNewLine: bool) -> int** - adds a new line to the array of strings, field "createNewLine"
          is responsible for creating a new line at the end, returns the position of the new line in the array
        - **clearSpace(i: int, createNewLine: bool)** - clears the line with number "i", field "createNewLine" is responsible for
          creating a newline at the end
        - **changeSpace(i: int, text='', createNewLine=True)** - changes the properties of the i-th line to new ones
    - **Vec3 class**:
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
        - **setLocalPosition(V: Vec3)** - move local position to "V" vector, adjusted for physics
        - **getPosition()** - get the global position of the object in the world
    - **obj class**:
        - **isInstantiated: bool** - determines if the object was created using the instantiate() method
        - **tr: Transform** - Transform class
        - **GetComponent(typ: Component)** - allows you to get a component of type "typ"
        - **AddComponent(comp: Component)** - allows you to create a "comp" type component
        - **AddComponents(comps: list)** - allows you to create "comps" components, of type "Component"
        - **AddCreatedComponent(comp)** - allows you to create a "comp" component
        - **GetAllComponentsOfType(typ: Component)** - allows you to get all components of type "typ"
        - **RemoveComponent(typ: Component)** - allows you to remove a component of type "typ"
        - **PopComponent(i: int)** - allows you to remove the component in place of "i"
    - **Drawer class**:
        - **drawSymb(a, symb: str, pos: Vec3)** - used to draw symbol "symb" at position "pos", works
          only in "lateUpdate"
        - **clearSymb(a, pos: Vec3)** - used to clear symbol at position "pos", only works in "
          onDraw"
    - **Behavior class**:
        - **update(self, a)** - called every world update
        - **start(self)** - called at the very beginning
        - **onCollide(self, collider: Transform)** - called on contact with an object
        - **lateUpdate(self, a):** - called after "update"
        - **passSteps(frames: int)** - used to completely stop the object for "frames" ticks
        - **passSeconds(secs: float)** - used to completely stop the object for "secs" seconds
        - **instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj** - used to create objects at position "Pos" with
          components "comps" and symbol "symb"
        - **destroy(beh)** - removes the object "beh" from the world
    - **clamp(num, min_value, max_value)** - the simplest variable constraint
    - **findAllObjsAtRad(V: Vec3, rad: float)** - returns objects in radius "rad" to position "V"
    - **findNearObjByRad(V: Vec3, rad: float)** - returns the closest object within radius "rad" to position "V"

# That's all! Thanks for reading!