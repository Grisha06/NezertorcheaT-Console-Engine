# NezertorcheaT's Console Engine

## Вітаю вас в документації по Nezertorcheat's Console Engine!

Щоб спробувати тестовий проект, запустіть файл main.py.

Редактор мапи представлений списком JSON файлів в папці Maps.  
Перше поле-це ім'я мапи.  
Далі йдуть опису ігрових об'єктів, а конкретніше їх імен.  
Усередині об'єктів знаходяться поля " * * startPos **" і "**components**".  
Перше-це представлення початкової позиції як вектора.  
Друге-це список компонентів.  
У ньому можуть лежати будь-які об'єкти типи яких успадковані від класу"**Component**".  
А в ньому можуть лежати властивості цих об'єктів.

## Тепер найцікавіше! Свої скрипти!

В папці Scripts ви можете створювати свої файли, за подобою наявних. Ваш скрипт повинен виглядати ось так:

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

### Пояснення звичайних методів і КЛАСІВ:

1. NTETime:
    - **getTime () * * - повертає поточний кадр
2. ObjList:
    - **getObjs () * * - отримати всі об'єкти
3. globalSettings:
    - **settings * * - всі поля з файлу globalSettings.json
    - **objMaps * * - мапи з папки Maps
4. NTEmapManager:
    - **loadLevel (mapname: str = "globalMap") * * - завантажує мапу, що зберігається в папці Maps, з ім'ям "mapname"
    - **stopMainLoop (func) * * - зупиняє головний цикл, прокинувши помилку, але, перед цим, виконує функцію "func"
5. NTEngineClasses:
    - **об'єкт ui * * - представлення класу UI
    - **клас UI**:
        - **add (text, createNewLine: bool) - > int * * - додає новий рядок в масив рядків, поле "createNewLine" відповідає за створення нового рядка в кінці, повертає позицію нового рядка в масиві
        - **clearSpace (I: int, createNewLine: bool) * * - очищає рядок з номером "i", поле "createNewLine" відповідає за створення нового рядка в кінці
        - **changeSpace (I: int, text=", createNewLine=True) * * - змінює властивості рядка з номером i на нові
        - **UI.printStrAtPos (s: str, x: int, y: int)** - вимальовує рядок в консолі, **увага!** Для відтворення об'єктів в ігровому світі використовуйте клас"Drawer"!
        - **UI.printImageAtPos (img: str, x: int, y: int) * * - відтворює зображення з ім'ям " img " в консолі, * * увага!** Для відтворення об'єктів в ігровому світі використовуйте клас"Drawer"!
    - **клас Component**:
        - **gameobject: Obj * * - посилання на об'єкт
    - **клас Vector3**:
        - **Vector3.dev_by_float (a, n=1) * * - оператор "* * / / * * "- ділить вектор" a "на число"n"
        - **Vec3.mult_by_float (a, n=0) * * - оператор "* * % * * "- примножує вектор" a "на число"n"
        - **Vector3.sum (a, b) * * - оператор "* * + * * "- сума векторів " a " і "b"
        - **Vector3.substr(a, b)** - оператор "**-**" - з вектора "a" вычетает вектор "b"
        - **Vector3.mult (a, b) * * - оператор " * "- множить компоненти вектора " a "на компоненти вектора "b"
        - **Vector3.div (a, b) * * - ділить компоненти вектора " a "на компоненти вектора "b"
        - **Vector3.distance (v1, v2) * * - відстань між векторами " v1 " і "v2"
        - **Vector3.dot (a, b) * * - оператор "* * "- Скалярний добуток векторів " a " і "b"
        - **Vector3.reflect(rd, n)**
        - **length () * * - довжина вектора
        - **abs()**
        - **norm()**
        - **sign()**
    - **клас Obj**:
        - **isInstantiated: bool * * - визначає, чи був об'єкт створений за допомогою методу instantiate ()
        - **tr: Transform * * - клас Transform
        - **GetComponent (Typ: Component) * * - дозволяє отримати компонент типу "typ"
        - **AddComponent(comp: Component) * * - дозволяє створити компонент типу "comp"
        - **AddComponents (comps: list) * * - дозволяє створити компоненти "comps", типу "Component"
        - **AddCreatedComponent (comp) * * - дозволяє створити компонент "comp"
        - **GetAllComponentsOfType (Typ: Component) * * - дозволяє отримати всі компоненти типу "typ"
        - **RemoveComponent (Typ: Component) * * - дозволяє видалити компонент типу "typ"
        - **PopComponent (I: int) * * - дозволяє видалити компонент на місці "i"
        - **Find (name: str) * * - дозволяє знайти об'єкт по імені
        - **FindByTag (tag: str) * * - дозволяє знайти об'єкт за тегом
        - **FindWithComponent (comp: Component) * * - дозволяє знайти об'єкт по компоненту
        - **FindAllWithComponent (comp: Component) * * - дозволяє знайти всі об'єкти з компонентом
        - **FindAllByTag (tag: str) * * - дозволяє знайти всі об'єкти з тегом
    - **clamp (num, min_value, max_value) * * - найпростіше обмеження змінної
    - **findAllObjsAtRad(V: Vec3, rad: float) * * - повертає об'єкти В радіусі "rad" до позиції"V"
    - **findNearObjByRad(V: Vec3, rad: float) * * - повертає найближчий об'єкт В радіусі "rad" до позиції"V"

### Пояснення компонентів:

Це були звичайні класи і методи використовуються повсюдно, а тепер йдуть ті, які я буду називати
компонентами, оскільки всі успадковані від класу"Component".  
Вони використовуються при описі поведінки об'єктів.  
З ними можна взаємодіяти через методи класу "Obj".  
Так само у них у всіх є посилання на об'єкт до якого вони прив'язані.

1. ** клас Transform**:
    - **local_position: Vec3 * * - локальна позиція об'єкта
    - **position: Vec3 * * - Глобальна позиція об'єкта
    - **moweDir (Dir: Vec3) * * - додати до позиції вектор "Dir"
    - **setLocalPosition (V: Vec3) * * - перемістити локальну позицію в вектор "V"
2. ** клас Drawer**:
    - **drawSymb(a, symb: str, pos: Vec3) * * - використовується для відтворення символу "symb" на позиції "pos", працює тільки в "lateUpdate"
    - **clearSymb (a, pos: Vec3) * * - використовується для очищення символу на позиції "pos", працює тільки в "onDraw"
3. ** клас Camera**:
    - **offset * * - зміщення камери від лівого кута, спочатку дорівнює половині розміру отрисовываемой мапи
4. ** клас BoxCollider**:
    - **height * * - висота колайдера
    - **width** - ширина коллайдера
    - **collide * * - зіткнення
5. ** клас RigidBody * * - моя спроба реалізації фізики
6. ** клас Behavior**:
    - **update (self, a) * * - викликається кожне оновлення світу
    - **start (self) * * - викликається на самому початку
    - **onCollide (self, collider: Collider) * * - викликається при зіткненні з об'єктом
    - **lateUpdate (self, a): * * - викликається після "update"
    - **onDraw (self, a): * * - викликається після відтворення
    - **passSteps(frames: int) * * - використовується для повної зупинки об'єкта на "frames" тиків
    - **passSeconds(secs: float) * * - використовується для повної зупинки об'єкта на" secs " секунд
    - **instantiate (symb: str, Pos=Vec3 (), comps= []) - > Obj** - використовується для створення об'єктів в позиції " Pos "з компонентами" comps "і символом "symb"
    - **destroy (beh) * * - видаляє об'єкт "beh" зі світу

### Рада:

1. На сцені повинна бути хоча б одна камера, якщо їх немає, то нічого не буде намальовано.
2. Для визначення головної камери існує тег " * * MainCamera**".
3. Не використовуйте методи з * * ObjList**, замість них використовуйте * * Obj.Find () * * та ін.
4. Не використовуйте * * NTETime**.
5. Колізія поки погано реалізована, з цього вам доведеться писати її самостійно.
7. Приклад реалізації колізії:
```
class SomeBody(RigidBody):
    def updRB(self):
        for i in self.gameobject.transform.nears:
            for j in i.GetAllComponentsOfTypes(all_subclasses(RigidBody)):
                for jj in j.gameobject.GetAllComponentsOfType(Collider):
                    if jj.collide:
                        self.gameobject.transform.moveDir(Vector3.D2V(jj.angle - 1))
```

# На цьому все! Дякую за прочитання!