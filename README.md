# NezertorcheaT's Console Engine

## Welcome to NezertorcheaT's Console Engine documentation!

To try out a test project, run the main.py file.

The map editor is represented by a list of json files in the Maps folder.  
The first field is the name of the map.  
Further there are descriptions of game objects, and more specifically their names.  
Inside the objects are the "**startPos**" and "**components**" fields.  
The first is the representation of the starting position as a vector.  
The second is the list of components.  
It can contain any objects whose types are inherited from the "**Component**" class.  
And it can contain the properties of these objects.

The map editor is also represented by a graphical script written in python kivy.  
To use it, you need to run the kivy_redactor.py file.  
Interface example:  
![](https://github.com/Grisha06/NezertorcheaT-Console-Engine/blob/main/README_images/image.jpg?raw=true)
On the left you see a list of available objects.  
The **Add New Object** button will allow you to create a new object.  
The **Save Map** button will save the map as a .json file.  
Clicking on one of the objects in the list will select it.  
In the middle is an approximate map that should turn out in the game.  
By clicking on one of the objects on the map you select it.  
On the right you see the properties panel.  
The top properties are required.  
Namely:  
**Name** - name;  
**Layer** - rendering layer;  
**Tag** - tag.  
These properties are required for an object.  
There is also a **Transform** component required for an object.
It cannot be removed.  
The **local_position** property of the **Transform** component changes the local position of the object.  
There is also usually a Drawer component.  
Components can be deleted by clicking the **Delete** button next to the component name.  
The components are explained below.  
The **Add Component** button allows you to add one of the available components.  
The **Delete Object** button will allow you to delete the object.  

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

    def onCollide(self, collider: Collider):
        #<code>

    def onDraw(self, a):
        #<ui_code>
        #<draw_code>: Drawer().drawSymb(a, "8", Vec3(1, 1))
        
```

### Explanation of common methods and classes:

1. NTETime:
    - **getTime()** - returns the current frame
2. ObjList:
    - **getObjs()** - get all objects
3.globalSettings:
    - **settings** - all fields from the globalSettings.json file
    - **objMaps** - maps from Maps folder
4.NTEmapManager:
    - **loadLevel(mapname: str = "globalMap")** - loads the map stored in the Maps folder with the name "mapname"
    - **stopMainLoop(func)** - stops the main loop by throwing an error, but before that, executes the function "func"
5.NTEngineClasses:
    - **object ui** - representation of the UI class
    - **UI class**:
        - **add(text, createNewLine: bool) -> int** - adds a new line to the array of strings, the "createNewLine" field is responsible for creating a new line at the end, returns the position of the new line in the array
        - **clearSpace(i: int, createNewLine: bool)** - clears the line with the number "i", the "createNewLine" field is responsible for creating a new line at the end
        - **changeSpace(i: int, text='', createNewLine=True)** - changes the properties of the i-th line to new ones
        - **UI.printStrAtPos(s: str, x: int, y: int)** - draws a string in the console, **Attention!** To draw objects in the game world, use the "Drawer" class!
        - **UI.printImageAtPos(img: str, x: int, y: int)** - draws an image named "img" in the console, **Attention!** Use the "Drawer" class to draw objects in the game world!
    - **Component class**:
        - **gameobject: Obj** - object reference
    - **Vector3 class**:
        - **Vector3.dev_by_float(a, n=1)** - operator "**//**" - divides vector "a" by number "n"
        - **Vec3.mult_by_float(a, n=0)** - operator "**%**" - multiplies vector "a" by number "n"
        - **Vector3.sum(a, b)** - operator "**+**" - sum of vectors "a" and "b"
        - **Vector3.substr(a, b)** - operator "**-**" - subtracts vector "b" from vector "a"
        - **Vector3.mult(a, b)** - operator "*" - multiplies the components of the vector "a" by the components of the vector "b"
        - **Vector3.div(a, b)** - divides the components of the vector "a" into the components of the vector "b"
        - **Vector3.distance(v1, v2)** - distance between vectors "v1" and "v2"
        - **Vector3.dot(a, b)** - operator "**" - Scalar product of vectors "a" and "b"
        - **Vector3.reflect(rd, n)**
        - **length()** - vector length
        - **abs()**
        - **normal()**
        - **sign()**
    - **obj class**:
        - **isInstantiated: bool** - determines if the object was created using the instantiate() method
        - **tr: Transform** - Transform class
        - **GetComponent(typ: Component)** - allows you to get a component of type "type"
        - **AddComponent(comp: Component)** - allows you to create a "comp" type component
        - **AddComponents(comps: list)** - allows you to create "comps" components, of type "Component"
        - **AddCreatedComponent(comp)** - allows you to create a "comp" component
        - **GetAllComponentsOfType(typ: Component)** - allows you to get all components of type "typ"
        - **RemoveComponent(typ: Component)** - allows you to remove a component of type "typ"
        - **PopComponent(i: int)** - allows you to remove the component in place of "i"
        - **Find(name: str)** - allows you to find an object by name
        - **FindByTag(tag: str)** - allows you to find an object by tag
        - **FindWithComponent(comp: Component)** - allows you to find an object by component
        - **FindAllWithComponent(comp: Component)** - allows you to find all objects with a component
        - **FindAllByTag(tag: str)** - allows you to find all objects with a tag
    - **clamp(num, min_value, max_value)** - the simplest variable constraint
    - **findAllObjsAtRad(V: Vec3, rad: float)** - returns objects in radius "rad" to position "V"
    - **findNearObjByRad(V: Vec3, rad: float)** - returns the closest object within radius "rad" to position "V"

### Explanation of components:

These were ordinary classes and methods used everywhere, and now there are those that I will call components, since all are inherited from the "Component" class.  
They are used in describing the behavior of objects.  
They can be interacted with through the methods of the "Obj" class.  
Also, they all have a link to the object to which they are attached.  

1. **Transform class**:
    - **local_position: Vec3** - local position of the object
    - **position: Vec3** - global position of the object
    - **moweDir(Dir: Vec3)** - add "Dir" vector to position
    - **setLocalPosition(V: Vec3)** - move local position to "V" vector
2. **Drawer class**:
    - **drawSymb(a, symb: str, pos: Vec3)** - used to draw symbol "symb" at position "pos", only works in "lateUpdate"
    - **clearSymb(a, pos: Vec3)** - used to clear symbol at position "pos", only works in "onDraw"
3. **Camera class**:
    - **offset** - camera offset from the left corner, initially equal to half the size of the rendered map
4. **BoxCollider class**:
    - **height** - collider height
    - **width** - collider width
    - **collide** - contact
5. **RigidBody class** - my attempt to implement physics
6. **Behavior class**:
    - **update(self, a)** - called every world update
    - **start(self)** - called at the very beginning
    - **onCollide(self, collider: Collider)** - called upon contact with an object
    - **lateUpdate(self, a):** - called after "update"
    - **onDraw(self, a):** - called after drawing
    - **passSteps(frames: int)** - used to completely stop the object for "frames" ticks
    - **passSeconds(secs: float)** - used to completely stop the object for "secs" seconds
    - **instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj** - used to create objects at position "Pos" with components "comps" and symbol "symb"
    - **destroy(beh)** - removes the object "beh" from the world

### Tips:

1. There must be at least one camera on the scene, if there are none, then nothing will be drawn.  
2. There is a "**MainCamera**" tag to define the main camera.  
3. Do not use methods from **ObjList**, use **Obj.Find()** instead, etc.  
4. Don't use **NTETime**.  
5. Collision is still poorly implemented, so you will have to write it yourself.  
7. An example of the implementation of a collision:  
```
class SomeBody(RigidBody):
    def updRB(self):
        for i in self.gameobject.transform.nears:
            for j in i.GetAllComponentsOfTypes(all_subclasses(RigidBody)):
                for jj in j.gameobject.GetAllComponentsOfType(Collider):
                    if jj collide:
                        self.gameobject.transform.moveDir(Vector3.D2V(jj.angle))
```

# That's all! Thanks for reading!