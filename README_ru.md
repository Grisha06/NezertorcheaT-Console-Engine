# NezertorcheaT Console Engine

## Приветствую вас в документации по NezertorcheaT Console Engine!

Чтобы попробовать тестовый проект, запустите файл main.py.

Редактор карты представлен списком json файлов в папке Maps.  
Первое поле - это имя карты.  
Далее идут описания игровых объектов, а конкретнее их имён.  
Внутри объектов находятся поля "**startPos**" и "**components**".  
Первое - это представление начальной позиции как вектора.  
Второе - это список компонентов.  
В нём могут лижать любые объекты типы которых наследованны от класса "**Component**".  
А в нём могут лижать свойства этих объектов.

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

    def onCollide(self, collider: Transform):
        pass

    def onDraw(self, a):
        #<ui_code>  
        #<draw_code>: Drawer().drawSymb(a, "8", Vec3(1, 1))
        
```  

### Объяснение методов:

1. NTETime:
    - **getTime()** - возвращает текущий кадр
2. ObjList:
    - **getObj(i: int)** - получить объект
    - **getObjs()** - получить все объекты
    - **getObjByName(name: str)** - получить объект с именем "name"
3. globalSettings:
    - **settings** - все поля из файла globalSettings.json
    - **objMaps** - карта из папки Maps
4. Drawer:
    - **drawSymb(a, symb: str, pos: Vec3)** - рисует символ "symb" в позиции "pos" на матрице "a"
    - **drawSymbImage(a, img: str, pos: Vec3)** - рисует список символов, хранящихся в папке TextImages, с именем "img"
      в позиции "pos" на матрице "a"
5. NTEmapManager:
    - **loadLevel(mapname: str = "globalMap")** - загружает карту, хранящуюся в папке Maps, с именем "mapname"
    - **stopMainLoop(func)** - останавливает главный цикл, пробросив ошибку, но, перед этим, выполняет функцию "func"
6. NTEngineClasses:
    - **объект ui** - представление класса UI
    - **объект camera** - представление класса Camera
    - **класс UI**:
        - **add(text, createNewLine: bool) -> int** - добавляет новую строку в массив строк, поле "createNewLine"
          отвечает за создание новой строки в конце, возвращает позицию новой строки в массиве
        - **clearSpace(i: int, createNewLine: bool)** - очищает строку с номером "i", поле "createNewLine" отвечает за
          создание новой строки в конце
        - **changeSpace(i: int, text='', createNewLine=True)** - изменяет свойства строки с номером i на новые
    - **класс Vec3**:
        - **Vec3.dev_by_float(a, n=1)** - оператор "**//**" - делит вектор "a" на число "n"
        - **Vec3.mult_by_float(a, n=0)** - оператор "**%**" - умножает вектор "a" на число "n"
        - **Vec3.sum(a, b)** - оператор "**+**" - сумма векторов "a" и "b"
        - **Vec3.substr(a, b)** - оператор "**-**" - из вектора "a" вычетает вектор "b"
        - **Vec3.mult(a, b)** - оператор "*" - умножает компоненты вектора "a" на компоненты вектора "b"
        - **Vec3.div(a, b)** - делит компоненты вектора "a" на компоненты вектора "b"
        - **Vec3.distance(v1, v2)** - расстояние между векторами "v1" и "v2"
        - **Vec3.dot(a, b)** - оператор "**" - Скалярное произведение векторов "a" и "b"
        - **Vec3.reflect(rd, n)**
        - **length()** - длинна вектора
        - **abs()**
        - **norm()**
        - **sign()**
    - **класс Transform**:
        - **local_position: Vec3** - локальная позиция объекта
        - **collide: bool** - просчет столкновений
        - **beh: Behavior** - ссылка на поведение
        - **moweDir(Dir: Vec3)** - прибавить к позиции вектор "Dir", с поправкой на физику
        - **setLocalPosition(V: Vec3)** - переместить локальную позицию в вектор "V", с поправкой на физику
        - **getPosition()** - получить глобальную позицию объекта в мире
    - **класс Obj**:
        - **isInstantiated: bool** - определяет был ли объект создан с помощью метода instantiate()
        - **tr: Transform** - класс Transform
        - **GetComponent(typ: Component)** - позволяет получить компонент типа "typ"
        - **AddComponent(comp: Component)** - позволяет создать компонент типа "comp"
        - **AddComponents(comps: list)** - позволяет создать компоненты "comps", типа "Component"
        - **AddCreatedComponent(comp)** - позволяет создать компонент "comp"
        - **GetAllComponentsOfType(typ: Component)** - позволяет получить все компоненты типа "typ"
        - **RemoveComponent(typ: Component)** - позволяет удалить компонент типа "typ"
        - **PopComponent(i: int)** - позволяет удалить компонент на месте "i"
    - **класс Drawer**:
        - **drawSymb(a, symb: str, pos: Vec3)** - используется для отрисовки символа "symb" на позиции "pos", работает
          только в "lateUpdate"
        - **clearSymb(a, pos: Vec3)** - используется для очищения символа на позиции "pos", работает только в "
          onDraw"
    - **класс Behavior**:
        - **update(self, a)** - вызывается каждое обновление мира
        - **start(self)** - вызывается в самом начале
        - **onCollide(self, collider: Transform)** - вызывается при соприкосновении с объектом
        - **lateUpdate(self, a):** - вызывается после "update"
        - **passSteps(frames: int)** - используется для полной остановки объекта на "frames" тиков
        - **passSeconds(secs: float)** - используется для полной остановки объекта на "secs" секунд
        - **instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj** - используется для создания объектов в позиции "Pos" с
          компонентами "comps" и символом "symb"
        - **destroy(beh)** - удаляет объект "beh" из мира
    - **clamp(num, min_value, max_value)** - простейшее ограничение переменной
    - **findAllObjsAtRad(V: Vec3, rad: float)** - возвращает объекты в радиусе "rad" к позиции "V"
    - **findNearObjByRad(V: Vec3, rad: float)** - возвращает ближайший объект в радиусе "rad" к позиции "V"

# На этом всё! Спасибо за прочтение!
