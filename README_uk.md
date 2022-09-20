# NezertorcheaT Console Engine

## Вітаю вас у документації з NezertorcheaT Console Engine!

Щоб спробувати тестовий проект, запустіть файл main.py.

Редактор картки представлений списком json файлів у папці Maps.
Перше поле – це ім'я мапи.
Далі йдуть описи ігрових об'єктів, а конкретніше їх імен.
Всередині об'єктів знаходяться поля "**startPos**" та "**components**".
Перше – це уявлення початкової позиції як вектора.
Друге – це список компонентів.
У ньому можуть лижати будь-які об'єкти, типи яких успадковані від класу "Component".
А в ньому можуть лижати властивості цих об'єктів.

## Тепер найцікавіше! Свої скрипти!

У папці Scripts ви можете створювати свої файли, подібні до наявних. Ваш скрипт має виглядати так:

````
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
        
````

### Пояснення методів:

1. NTETime:
    - **getTime()** - повертає поточний кадр
2. ObjList:
    - **getObj(i: int)** - отримати об'єкт
    - **getObjs()** - отримати всі об'єкти
    - **getObjByName(name: str)** - отримати об'єкт з ім'ям "name"
3. GlobalSettings:
    - **settings** - усі поля з файлу globalSettings.json
    - **objMaps** - мапа з папки Maps
4. Drawer:
    - **drawSymb(a, symb: str, pos: Vec3)** - малює символ "symb" у позиції "pos" на матриці "a"
    - **drawSymbImage(a, img: str, pos: Vec3)** - малює список символів, що зберігаються в папці TextImages, з ім'ям "img"
      у позиції "pos" на матриці "a"
5. NTEmapManager:
    - **loadLevel(mapname: str = "globalMap")** - завантажує мапу, що зберігається в папці Maps, з ім'ям "mapname"
    - **stopMainLoop(func)** - зупиняє головний цикл, прокинувши помилку, але, перед цим, виконує функцію "func"
6. NTEngineClasses:
    - **об'єкт ui** - представлення класу UI
    - **об'єкт camera** - представлення класу Camera
    - **клас UI**:
        - **add(text, createNewLine: bool) -> int** - додає новий рядок у масив рядків, поле "createNewLine"
          відповідає за створення нового рядка в кінці, повертає позицію нового рядка в масиві
        - **clearSpace(i: int, createNewLine: bool)** - очищає рядок з номером "i", поле "createNewLine" відповідає за
          створення нового рядка наприкінці
        - **changeSpace(i: int, text='', createNewLine=True)** - змінює властивості рядка з номером i на нові
    - **клас Vec3**:
        - **Vec3.dev_by_float(a, n=1)** - ділить вектор "a" на число "n"
        - **Vec3.mult_by_float(a, n=0)** - множить вектор "a" на число "n"
        - **Vec3.sum(a, b)** - сума векторів "a" та "b"
        - **Vec3.substr(a, b)** - з вектора "a" вичістає вектор "b"
        - **Vec3.mult(a, b)** - множить компоненти вектора "a" на компоненти вектора "b"
        - **Vec3.div(a, b)** - ділить компоненти вектора "a" на компоненти вектора "b"
        - **Vec3.distance(v1, v2)** - відстань між векторами "v1" та "v2"
        - **Vec3.dot(a, b)** - Скалярний добуток векторів "a" та "b"
        - **Vec3.reflect(rd, n)**
        - **length()** - довжина вектора
        - **abs()**
        - **norm()**
        - **sign()**
    - **клас Transform**:
        - **local_position: Vec3** - локальна позиція об'єкта
        - **collide: bool** - прорахунок зіткнень
        - **beh: Behavior** - посилання на поведінку
        - **moweDir(Dir: Vec3)** - додати до позиції вектор "Dir", з поправкою на фізику
        - **setLocalPosition(V: Vec3)** - перемістити локальну позицію у вектор "V", з поправкою на фізику
        - **getPosition()** - отримати глобальну позицію об'єкта у світі
    - **клас Obj**:
        - **isInstantiated: bool** - визначає чи був об'єкт створений за допомогою методу instantiate()
        - **tr: Transform** - клас Transform
        - **GetComponent(typ: Component)** - дозволяє отримати компонент типу "typ"
        - **AddComponent(comp: Component)** - дозволяє створити компонент типу "comp"
        - **AddComponents(comps: list)** - дозволяє створити компоненти "comps", типу "Component"
        - **AddCreatedComponent(comp)** - дозволяє створити компонент "comp"
        - **GetAllComponentsOfType(typ: Component)** - дозволяє отримати всі компоненти типу "typ"
        - **RemoveComponent(typ: Component)** - дозволяє видалити компонент типу "typ"
        - **PopComponent(i: int)** - дозволяє видалити компонент на місці "i"
    - **клас Drawer**:
        - **drawSymb(a, symb: str, pos: Vec3)** - використовується для відображення символу "symb" на позиції "pos", працює
          тільки в "lateUpdate"
        - **clearSymb(a, pos: Vec3)** - використовується для очищення символу на позиції "pos", працює тільки в "
          onDraw"
    - **клас Behavior**:
        - **update(self, a)** - викликається кожне оновлення всесвіта
        - **start(self)** - викликається на самому початку
        - **onCollide(self, collider: Transform)** - викликається при зіткненні з об'єктом
        - **lateUpdate(self, a):** - викликається після "update"
        - **passSteps(frames: int)** - використовується для повної зупинки об'єкта на "frames" тиків
        - **passSeconds(secs: float)** - використовується для повної зупинки об'єкта на "secs" секунд
        - **instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj** - використовується для створення об'єктів у позиції "Pos" з
          компонентами "comps" та символом "symb"
        - **destroy(beh)** - видаляє об'єкт "beh" зі світу
    - **clamp(num, min_value, max_value)** - найпростіше обмеження змінної
    - **findAllObjsAtRad(V: Vec3, rad: float)** - повертає об'єкти в радіусі "rad" до позиції "V"
    - **findNearObjByRad(V: Vec3, rad: float)** - повертає найближчий об'єкт у радіусі "rad" до позиції "V"

# На цьому все! Дякую за прочитання!