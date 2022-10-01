# NezertorcheaT's Console Engine

## Приветствую вас в документации по NezertorcheaT's Console Engine!

Чтобы попробовать тестовый проект, запустите файл main.py.

Редактор карты представлен списком json файлов в папке Maps.  
Первое поле - это имя карты.  
Далее идут описания игровых объектов, а конкретнее их имён.  
Внутри объектов находятся поля "**startPos**" и "**components**".  
Первое - это представление начальной позиции как вектора.  
Второе - это список компонентов.  
В нём могут лежать любые объекты типы которых наследованы от класса "**Component**".  
А в нём могут лежать свойства этих объектов.

## Теперь самое интересное! Cвои скрипты!

В папке Scripts вы можете создавать свои файлы, по подобию имеющихся. Ваш скрипт должен выглядеть вот так:

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

### Объяснение обычных методов и классов:

1. NTETime:
    - **getTime()** - возвращает текущий кадр
2. ObjList:
    - **getObjs()** - получить все объекты
3. globalSettings:
    - **settings** - все поля из файла globalSettings.json
    - **objMaps** - карты из папки Maps
4. NTEmapManager:
    - **loadLevel(mapname: str = "globalMap")** - загружает карту, хранящуюся в папке Maps, с именем "mapname"
    - **stopMainLoop(func)** - останавливает главный цикл, пробросив ошибку, но, перед этим, выполняет функцию "func"
5. NTEngineClasses:
    - **объект ui** - представление класса UI
    - **класс UI**:
        - **add(text, createNewLine: bool) -> int** - добавляет новую строку в массив строк, поле "createNewLine" отвечает за создание новой строки в конце, возвращает позицию новой строки в массиве
        - **clearSpace(i: int, createNewLine: bool)** - очищает строку с номером "i", поле "createNewLine" отвечает за создание новой строки в конце
        - **changeSpace(i: int, text='', createNewLine=True)** - изменяет свойства строки с номером i на новые
        - **UI.printStrAtPos(s: str, x: int, y: int)** - отрисовывает строку в консоли, **Внимание!** Для отрисовки объектов в игровом мире используйте класс "Drawer"!
        - **UI.printImageAtPos(img: str, x: int, y: int)** - отрисовывает изображение с именем "img" в консоли, **Внимание!** Для отрисовки объектов в игровом мире используйте класс "Drawer"!
    - **класс Component**:
        - **gameobject: Obj** - ссылка на объект
    - **класс Vector3**:
        - **Vector3.dev_by_float(a, n=1)** - оператор "**//**" - делит вектор "a" на число "n"
        - **Vec3.mult_by_float(a, n=0)** - оператор "**%**" - умножает вектор "a" на число "n"
        - **Vector3.sum(a, b)** - оператор "**+**" - сумма векторов "a" и "b"
        - **Vector3.substr(a, b)** - оператор "**-**" - из вектора "a" вычетает вектор "b"
        - **Vector3.mult(a, b)** - оператор "*" - умножает компоненты вектора "a" на компоненты вектора "b"
        - **Vector3.div(a, b)** - делит компоненты вектора "a" на компоненты вектора "b"
        - **Vector3.distance(v1, v2)** - расстояние между векторами "v1" и "v2"
        - **Vector3.dot(a, b)** - оператор "**" - Скалярное произведение векторов "a" и "b"
        - **Vector3.reflect(rd, n)**
        - **length()** - длинна вектора
        - **abs()**
        - **norm()**
        - **sign()**
    - **класс Obj**:
        - **isInstantiated: bool** - определяет, был ли объект создан с помощью метода instantiate()
        - **tr: Transform** - класс Transform
        - **GetComponent(typ: Component)** - позволяет получить компонент типа "typ"
        - **AddComponent(comp: Component)** - позволяет создать компонент типа "comp"
        - **AddComponents(comps: list)** - позволяет создать компоненты "comps", типа "Component"
        - **AddCreatedComponent(comp)** - позволяет создать компонент "comp"
        - **GetAllComponentsOfType(typ: Component)** - позволяет получить все компоненты типа "typ"
        - **RemoveComponent(typ: Component)** - позволяет удалить компонент типа "typ"
        - **PopComponent(i: int)** - позволяет удалить компонент на месте "i"
        - **Find(name: str)** - позволяет найти объект по имени
        - **FindByTag(tag: str)** - позволяет найти объект по тегу
        - **FindWithComponent(comp: Component)** - позволяет найти объект по компоненту
        - **FindAllWithComponent(comp: Component)** - позволяет найти все объекты с компонентом
        - **FindAllByTag(tag: str)** - позволяет найти все объекты с тегом
    - **clamp(num, min_value, max_value)** - простейшее ограничение переменной
    - **findAllObjsAtRad(V: Vec3, rad: float)** - возвращает объекты в радиусе "rad" к позиции "V"
    - **findNearObjByRad(V: Vec3, rad: float)** - возвращает ближайший объект в радиусе "rad" к позиции "V"

### Объяснение компонентов:

Это были обыкновенные классы и методы использующиеся повсеместно, а теперь идут те, которые я буду называть
компонентами, так как все наследованы от класса "Component".  
Они используются при описании поведения объектов.  
С ними можно взаимодействовать через методы класса "Obj".  
Так же у них у всех есть ссылка на объект к которому они привязаны.

1. **класс Transform**:
    - **local_position: Vec3** - локальная позиция объекта
    - **position: Vec3** - глобальная позиция объекта
    - **moweDir(Dir: Vec3)** - прибавить к позиции вектор "Dir"
    - **setLocalPosition(V: Vec3)** - переместить локальную позицию в вектор "V"
2. **класс Drawer**:
    - **drawSymb(a, symb: str, pos: Vec3)** - используется для отрисовки символа "symb" на позиции "pos", работает только в "lateUpdate"
    - **clearSymb(a, pos: Vec3)** - используется для очищения символа на позиции "pos", работает только в "onDraw"
3. **класс Camera**:
    - **offset** - смещение камеры от левого угла, первоначально равно половине размера отрисовываемой карты
4. **класс BoxCollider**:
    - **height** - высота коллайдера
    - **width** - ширина коллайдера
    - **collide** - соприкосновение
5. **класс RigidBody** - моя попытка реализации физики
6. **класс Behavior**:
    - **update(self, a)** - вызывается каждое обновление мира
    - **start(self)** - вызывается в самом начале
    - **onCollide(self, collider: Collider)** - вызывается при соприкосновении с объектом
    - **lateUpdate(self, a):** - вызывается после "update"
    - **onDraw(self, a):** - вызывается после отрисовки
    - **passSteps(frames: int)** - используется для полной остановки объекта на "frames" тиков
    - **passSeconds(secs: float)** - используется для полной остановки объекта на "secs" секунд
    - **instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj** - используется для создания объектов в позиции "Pos" с компонентами "comps" и символом "symb"
    - **destroy(beh)** - удаляет объект "beh" из мира

### Советы:

1. На сцене должна быть хотя бы одна камера, если их нет, то ничего не будет отрисовано.
2. Для определения главной камеры существует тег "**MainCamera**".
3. Не используйте методы из **ObjList**, вместо них используйте **Obj.Find()** и др.
4. Не используйте **NTETime**.
5. Коллизия пока плохо реализована, по этому вам придется писать её самостоятельно.
7. Пример реализации коллизии:
```
class SomeBody(RigidBody):
    def updRB(self):
        for i in self.gameobject.transform.nears:
            for j in i.GetAllComponentsOfTypes(all_subclasses(RigidBody)):
                for jj in j.gameobject.GetAllComponentsOfType(Collider):
                    if jj.collide:
                        self.gameobject.transform.moveDir(Vector3.D2V(jj.angle - 1))
```

# На этом всё! Спасибо за прочтение!