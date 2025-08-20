# Section 2: Classes 🏗️

## 🎯 Learning Objectives
- [x] Understand Python's object model and how classes work internally ✅ 2025-08-20
- [x] Master the difference between class and instance attributes ✅ 2025-08-20
- [ ] Learn how method binding works in Python
- [ ] Implement properties for controlled attribute access
- [ ] Know when to use class methods, static methods, and instance methods
- [ ] Understand class body scope and namespace behavior
- [ ] Create and manipulate attributes at runtime
- [ ] Use UML to model class relationships

---

## 📖 Key Concepts

### **Notebook 01: Objects and Classes** 🏗️

**Core Concept**: Everything in Python is an object, including classes themselves. Classes are blueprints for creating objects.

#### **Python Object Model**
```
┌─────────────────┐    ┌─────────────────┐
│      type       │───▶│   metaclass     │
│  (metaclass)    │    │   hierarchy     │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│    MyClass      │───▶│   instances     │
│   (class)       │    │   (objects)     │
└─────────────────┘    └─────────────────┘
```

#### **UML Class Diagram - Basic Object Relationships**
```
┌─────────────┐
│    type     │
│<<metaclass>>│
└─────────────┘
       △
       │
┌─────────────┐
│   Person    │
├─────────────┤
│             │
├─────────────┤
│             │
└─────────────┘
       △
       │ creates
┌─────────────┐
│  p: Person  │
│ <<instance>>│
└─────────────┘
```

#### **Key Points**:
- Classes are objects of type `type` 
- Instances are objects of the class type
- `type(obj)` vs `obj.__class__` (prefer `type()`)
- `isinstance(obj, Class)` for type checking
- `id()` shows object identity in memory

#### **Object Inspection Methods**:
```python
class Person:
    pass

p = Person()

# Type relationships
print(type(Person))      # <class 'type'>
print(type(p))          # <class '__main__.Person'>
print(isinstance(p, Person))  # True
print(isinstance(Person, type))  # True

# Object identity
print(id(p))            # Memory address
print(hex(id(p)))       # Hex format
```

#### **Dynamic Attribute Manipulation**:
```python
# Getting attributes
getattr(Person, '__name__', 'default')  # Safer than direct access
hasattr(Person, 'some_attr')            # Check existence

# Setting attributes
setattr(Person, 'new_attr', 'value')    # Dynamic assignment
Person.another_attr = 'direct'          # Direct assignment

# Deleting attributes
delattr(Person, 'new_attr')             # Dynamic deletion
del Person.another_attr                 # Direct deletion

# Viewing object state
print(Person.__dict__)  # Class namespace
print(vars(Person))     # Equivalent to __dict__
```

---

### **Notebook 02: Class Attributes** 📊

**Core Concept**: Class attributes are shared by all instances and live in the class namespace.

#### **UML Class Diagram - Class Attributes**
```
┌─────────────────────────┐
│       Program           │
├─────────────────────────┤
│ + language: str = "Python" │
│ + version: str = "3.10"    │
│ + author: str              │
├─────────────────────────┤
│                         │
└─────────────────────────┘
```

#### **Namespace Hierarchy**:
```python
class Program:
    language = 'Python'    # Class attribute
    version = '3.6'       # Class attribute

# Class namespace (mappingproxy - read-only view)
print(Program.__dict__)
# {'__module__': '__main__', 'language': 'Python', 'version': '3.6', ...}

# Dynamic attribute modification
Program.version = '3.7'   # Modifies class attribute
setattr(Program, 'x', 100)  # Adds new class attribute

# Attribute access methods
print(Program.language)              # Direct access
print(getattr(Program, 'language'))  # Dynamic access with optional default
```

#### **Key Insights**:
- Class attributes stored in `Class.__dict__` (mappingproxy)
- `mappingproxy` is read-only but can be modified via `setattr`/dot notation
- Not all attributes live in `__dict__` (e.g., `__name__` is stored elsewhere)
- Can add/modify/delete class attributes at runtime

---

### **Notebook 03: Callable Class Attributes** 🔧

**Core Concept**: Class attributes can be functions, which become the foundation for methods.

#### **UML Class Diagram - Methods as Attributes**
```
┌─────────────────────────┐
│       Person            │
├─────────────────────────┤
│                         │
├─────────────────────────┤
│ + say_hello(self): str  │
└─────────────────────────┘
```

#### **Function Storage in Class**:
```python
class Person:
    def say_hello(self):
        print(f'Hello from {self.name}!')

# Function is stored as class attribute
print(Person.__dict__['say_hello'])  # <function Person.say_hello at 0x...>
print(type(Person.say_hello))        # <class 'function'>

# Can be accessed like any other attribute
func = getattr(Person, 'say_hello')
print(func)  # Same function object
```

#### **Function vs Method Distinction**:
- **Class access**: `Person.say_hello` → function
- **Instance access**: `person.say_hello` → bound method
- Functions in class body are stored as regular functions
- Method binding happens at access time (descriptor protocol)

---

### **Notebook 04: Classes are Callable** 📞

**Core Concept**: Classes are callable objects that create and return new instances.

#### **UML Sequence Diagram - Instance Creation**
```
Client          Class           Instance
  │               │               │
  │─────call()────▶│               │
  │               │─────new()────▶│
  │               │               │
  │               │────init()────▶│
  │               │               │
  │◀──instance────│               │
```

#### **Instance Creation Process**:
```python
class Person:
    def say_hello(self):
        print(f'Hello from {self}!')

# Creating instances
p = Person()  # Class is callable

# Type verification
print(type(p))                    # <class '__main__.Person'>
print(isinstance(p, Person))      # True
print(p.__class__ is Person)      # True (but prefer type())
```

#### **Namespace Separation**:
```python
# Class vs Instance namespaces
print("Class dict:", Person.__dict__)      # Contains methods, class attributes
print("Instance dict:", p.__dict__)        # Initially empty, stores instance data

# Instance attributes don't affect class
p.name = "Alice"
print("After adding instance attr:", p.__dict__)  # {'name': 'Alice'}
print("Class dict unchanged:", Person.__dict__)   # Still no 'name'
```

#### **Important Gotcha - `__class__` vs `type()`**:
```python
class MyClass:
    __class__ = str  # Can be overridden!

m = MyClass()
print(type(m))       # <class '__main__.MyClass'> (correct)
print(m.__class__)   # <class 'str'> (misleading!)
```

---

### **Notebook 05: Data Attributes** 💾

**Core Concept**: Understanding attribute lookup order and the difference between class and instance attributes.

#### **UML Class Diagram - Attribute Lookup**
```
┌─────────────────────────┐
│     BankAccount         │
├─────────────────────────┤
│ + apr: float = 1.2      │ ← Class attribute
├─────────────────────────┤
│                         │
└─────────────────────────┘
           △
           │ creates
┌─────────────────────────┐
│   acc1: BankAccount     │
├─────────────────────────┤
│ + apr: float = 0        │ ← Instance attribute (shadows class)
│ + bank: str             │ ← Instance-only attribute
└─────────────────────────┘
```

#### **Attribute Lookup Algorithm**:
```
Instance Attribute Lookup:
1. Check instance.__dict__
2. If not found, check class.__dict__
3. If not found, check parent classes (MRO)
4. If not found, raise AttributeError
```

#### **Class vs Instance Attributes Example**:
```python
class BankAccount:
    apr = 1.2  # Class attribute - shared by all instances

acc_1 = BankAccount()
acc_2 = BankAccount()

# Both instances see the class attribute
print(acc_1.apr, acc_2.apr)  # 1.2, 1.2

# Modifying class attribute affects all instances
BankAccount.apr = 2.5
print(acc_1.apr, acc_2.apr)  # 2.5, 2.5

# Setting instance attribute shadows class attribute
acc_1.apr = 0
print(acc_1.apr, acc_2.apr)  # 0, 2.5

print(acc_1.__dict__)  # {'apr': 0}
print(acc_2.__dict__)  # {}
```

#### **Key Insights**:
- Instance attributes **shadow** class attributes
- Class attribute changes affect all instances (unless shadowed)
- Instance `__dict__` is a real dictionary (mutable)
- Class `__dict__` is a mappingproxy (read-only view)

---

### **Notebook 06: Function Attributes** ⚙️

**Core Concept**: How functions become methods through Python's descriptor protocol.

#### **UML Class Diagram - Method Binding**
```
┌─────────────────────────┐
│       Person            │
├─────────────────────────┤
│                         │
├─────────────────────────┤
│ + set_name(self, str)   │
└─────────────────────────┘
           △
           │
    ┌─────────────┐
    │ Descriptor  │
    │ Protocol    │
    └─────────────┘
```

#### **Function → Method Transformation**:
```python
class Person:
    def set_name(self, new_name):
        self.name = new_name

# When accessed from class: function
print(Person.set_name)           # <function Person.set_name at 0x...>
print(type(Person.set_name))     # <class 'function'>

# When accessed from instance: bound method
p = Person()
print(p.set_name)                # <bound method Person.set_name of <Person object>>
print(type(p.set_name))          # <class 'method'>

# Method object attributes
method = p.set_name
print(method.__self__)           # The instance (p)
print(method.__func__)           # The original function
```

#### **Method Binding Demonstration**:
```python
class Person:
    def say_hello(*args):  # Note: flexible arguments
        print('say_hello args:', args)

Person.say_hello()       # say_hello args: ()

p = Person()
p.say_hello()           # say_hello args: (<Person object>,)
                        # Instance is automatically passed as first argument!
```

#### **Manual Method Creation**:
```python
# Equivalent manual binding
Person.set_name(p, 'John')  # Same as p.set_name('John')

# This works because:
# p.set_name('John') 
# → becomes Person.set_name(p, 'John')
```

#### **Monkey Patching Methods**:
```python
# Adding methods to classes at runtime
Person.do_work = lambda self: f"Working from {self}"

# Both instances get the new method
p1 = Person()
p2 = Person()
print(p1.do_work())     # Bound method works!
print(p2.do_work())     # Works for all instances
```

#### **Instance vs Class Function Assignment**:
```python
# Adding function directly to instance (NOT a method)
p.other_func = lambda *args: print(f'Called with {args}')
print(p.other_func)     # <function <lambda> at 0x...> (NOT bound method)
p.other_func()          # Called with () (no self passed)

# vs adding to class (becomes method)
Person.class_func = lambda self: print(f'Method called on {self}')
p.class_func()          # Method called on <Person object> (self passed)
```

---

### **Notebook 07: Initializing Class Instances** 🔄

**Core Concept**: Understanding the two-phase instance creation: creation (`__new__`) and initialization (`__init__`).

#### **UML Sequence Diagram - Instance Initialization**
```
Client          Class         Instance
  │               │               │
  │────Person()───▶│               │
  │               │───__new__────▶│ (creates object)
  │               │               │
  │               │───__init__───▶│ (initializes object)
  │               │               │
  │◀─initialized──│               │
  │   instance     │               │
```

#### **The `__init__` Method**:
```python
class Person:
    def __init__(self, name):
        print(f'Initializing a new Person object: {self}')
        self.name = name  # Setting instance attribute

p = Person('Eric')
# Output: Initializing a new Person object: <__main__.Person object at 0x...>
print(hex(id(p)))  # Same memory address as shown in __init__
```

#### **Key Understanding**:
- `__init__` is an **instance method** (receives `self`)
- By the time `__init__` is called, the object **already exists**
- `__init__` doesn't return the instance (that's `__new__`'s job)
- `__init__` is for setting up initial state

#### **Manual vs Automatic Initialization**:
```python
# What happens automatically:
p = Person('Eric')
print(p.__dict__)  # {'name': 'Eric'}

# Manual equivalent:
class Person2:
    def initialize(self, name):
        self.name = name

p2 = Person2()
p2.initialize('Eric')  # Must call manually
print(p2.__dict__)     # {'name': 'Eric'}
```

---

### **Notebook 08: Creating Attributes at Run-Time** 🏃‍♂️

**Core Concept**: Dynamic attribute creation and the difference between functions and methods when added to instances.

#### **UML Class Diagram - Dynamic Method Binding**
```
┌─────────────────────────┐
│       Person            │
├─────────────────────────┤
│ + name: str             │
├─────────────────────────┤
│ + say_hello(): str      │ ← Added at runtime
└─────────────────────────┘

┌─────────────────────────┐
│    MethodType           │
│   <<utility>>           │
├─────────────────────────┤
│ + bind(func, instance)  │
└─────────────────────────┘
```

#### **Function vs Method on Instances**:
```python
class Person:
    def __init__(self, name):
        self.name = name

p1 = Person('Eric')

# Adding function directly to instance
p1.say_hello = lambda: 'Hello!'
print(p1.say_hello)     # <function <lambda> at 0x...> (function, not method)
print(p1.say_hello())   # 'Hello!' (works, but no self)

# Instance doesn't know about this function
p2 = Person('Alex')
# p2.say_hello()  # AttributeError!
```

#### **Creating Bound Methods with MethodType**:
```python
from types import MethodType

def say_hello(self):
    return f'{self.name} says hello!'

# Create bound method
p1_say_hello = MethodType(say_hello, p1)
print(p1_say_hello)     # <bound method say_hello of <Person object>>

# Add to instance
p1.say_hello = p1_say_hello
print(p1.say_hello())   # 'Eric says hello!'

# Still instance-specific
print(p2.__dict__)      # {} (doesn't have say_hello)
```

#### **Practical Example - Plugin Pattern**:
```python
class Person:
    def __init__(self, name):
        self.name = name
        
    def register_do_work(self, func):
        """Register a work function for this instance"""
        setattr(self, '_do_work', MethodType(func, self))
        
    def do_work(self):
        do_work_method = getattr(self, '_do_work', None)
        if do_work_method:
            return do_work_method()
        else:
            raise AttributeError('You must first register a do_work method')

# Usage
math_teacher = Person('Eric')
english_teacher = Person('John')

def work_math(self):
    return f'{self.name} will teach differentials today.'

def work_english(self):
    return f'{self.name} will analyze Hamlet today.'

# Register different work methods
math_teacher.register_do_work(work_math)
english_teacher.register_do_work(work_english)

print(math_teacher.do_work())    # Eric will teach differentials today.
print(english_teacher.do_work()) # John will analyze Hamlet today.
```

---

### **Notebook 09: Properties** 🎛️

**Core Concept**: Properties provide controlled access to attributes using getter/setter/deleter methods.

#### **UML Class Diagram - Property Pattern**
```
┌─────────────────────────┐
│       Person            │
├─────────────────────────┤
│ - _name: str            │ ← Private storage
├─────────────────────────┤
│ + name: str {property}  │ ← Public interface
│ + get_name(): str       │
│ + set_name(str): void   │
└─────────────────────────┘
```

#### **Basic Property Creation**:
```python
class Person:
    def __init__(self, name):
        self.name = name  # Uses property setter!
        
    def get_name(self):
        return self._name
    
    def set_name(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._name = value.strip()
        else:
            raise ValueError('name must be a non-empty string')
            
    name = property(fget=get_name, fset=set_name)

# Usage
p = Person('Alex')
print(p.name)           # 'Alex' (calls get_name)
p.name = 'John'         # (calls set_name)
# p.name = None         # ValueError: name must be a non-empty string
```

#### **Property Lookup Priority**:
```python
print(p.__dict__)       # {'_name': 'John'} (storage attribute)
print(Person.__dict__)  # Contains: 'name': <property at 0x...>

# Even if we manually add 'name' to instance dict:
p.__dict__['name'] = 'Hacker'
print(p.name)           # Still 'John' (property wins over instance attribute!)
```

#### **Property Benefits**:
- **Validation**: Control what values are accepted
- **Computed properties**: Calculate values on-the-fly
- **Backward compatibility**: Can change from simple attributes to properties
- **Logging/debugging**: Track attribute access

---

### **Notebook 10: Property Decorators** 🎭

**Core Concept**: Using the `@property` decorator syntax for cleaner property definitions.

#### **UML Class Diagram - Decorator Pattern**
```
┌─────────────────────────┐
│       Circle            │
├─────────────────────────┤
│ - _radius: float        │
├─────────────────────────┤
│ + radius: float {property}│
│ + area: float {readonly} │
│ + circumference: float   │
└─────────────────────────┘
```

#### **Property Decorator Syntax**:
```python
class Person:
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        """Get the person's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._name = value.strip()
        else:
            raise ValueError('name must be a non-empty string')
    
    @name.deleter
    def name(self):
        print('Deleting name...')
        del self._name

# Usage
p = Person('Alex')
print(p.name)           # Alex
p.name = 'John'         # Uses setter
del p.name              # Uses deleter
```

#### **How Decorator Syntax Works**:
```python
# This decorator syntax:
@property
def name(self):
    return self._name

# Is equivalent to:
def name(self):
    return self._name
name = property(name)

# And then:
@name.setter
def name(self, value):
    self._name = value

# Is equivalent to:
def name(self, value):
    self._name = value
name = name.setter(name)
```

#### **Advanced Property Example**:
```python
class Circle:
    def __init__(self, radius):
        self.radius = radius  # Uses property setter
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError('Radius must be positive')
        self._radius = value
        self._area = None  # Invalidate cached area
    
    @property
    def area(self):
        if self._area is None:
            print('Calculating area...')
            self._area = 3.14159 * (self._radius ** 2)
        return self._area
    
    @property
    def diameter(self):
        return self._radius * 2

c = Circle(5)
print(c.area)       # Calculating area... 78.53975
print(c.area)       # 78.53975 (cached)
c.radius = 3        # Invalidates cache
print(c.area)       # Calculating area... 28.27431
```

---

### **Notebook 11: Read-Only and Computed Properties** 📊

**Core Concept**: Creating properties that don't have setters (read-only) and properties that compute values dynamically.

#### **UML Class Diagram - Read-Only Properties**
```
┌─────────────────────────┐
│       Circle            │
├─────────────────────────┤
│ + radius: float         │
├─────────────────────────┤
│ + area: float {readonly}│
│ + circumference: float  │
│ {readonly}              │
└─────────────────────────┘
```

#### **Read-Only Properties**:
```python
from math import pi

class Circle:
    def __init__(self, radius):
        self.radius = radius
        
    @property
    def area(self):
        """Read-only computed property."""
        print('calculating area...')
        return pi * (self.radius ** 2)
    
    @property
    def circumference(self):
        """Another read-only computed property."""
        return 2 * pi * self.radius

c = Circle(1)
print(c.area)           # calculating area... 3.141592653589793
print(c.circumference)  # 6.283185307179586

# Can't set read-only properties
# c.area = 100          # AttributeError: can't set attribute
```

#### **Cached Computed Properties**:
```python
class Circle:
    def __init__(self, radius):
        self.radius = radius
        self._area = None
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        # Invalidate cache when radius changes
        self._area = None
        self._radius = value
        
    @property
    def area(self):
        if self._area is None:
            print('Calculating area...')
            self._area = pi * (self.radius ** 2)
        return self._area

c = Circle(1)
print(c.area)    # Calculating area... 3.141592653589793
print(c.area)    # 3.141592653589793 (from cache)

c.radius = 2     # Invalidates cache
print(c.area)    # Calculating area... 12.566370614359172
```

#### **Use Cases for Read-Only Properties**:
- **Computed values**: area, circumference, full name from first/last
- **Derived data**: age from birth date, file size from contents
- **Status information**: is_valid, is_complete, progress percentage
- **Aggregated data**: total, average, count from collections

---

### **Notebook 12: Deleting Properties** 🗑️

**Core Concept**: Understanding property deletion and implementing custom deletion behavior.

#### **Property Deletion Flow**:
```python
class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        print('getting name property value...')
        return self._name
    
    @name.setter
    def name(self, value):
        print(f'setting name property to {value}...')
        self._name = value
    
    @name.deleter
    def name(self):
        print('deleting name property value...')
        del self._name  # Delete the underlying storage

p = Person('Guido')
print(p.name)           # getting name property value... Guido
print(p.__dict__)       # {'_name': 'Guido'}

del p.name              # deleting name property value...
print(p.__dict__)       # {} (underlying _name is gone)

# p.name                # AttributeError: 'Person' object has no attribute '_name'
```

#### **Alternative Deletion Syntax**:
```python
# Using delattr function
p = Person('Raymond')
delattr(p, 'name')      # Same as 'del p.name'
```

#### **Important Notes**:
- Property deletion removes the **value**, not the **property definition**
- The property itself remains defined on the class
- Usually deletes underlying storage attribute(s)
- Can implement custom cleanup logic in deleter

---

### **Notebook 13: Class and Static Methods** 🏭

**Core Concept**: Understanding the three types of methods in Python classes and when to use each.

#### **UML Class Diagram - Method Types**
```
┌─────────────────────────┐
│       Timer             │
├─────────────────────────┤
│ + tz: timezone          │
├─────────────────────────┤
│ + current_dt_utc()      │ ← Static method
│ {static}                │
│ + set_tz(offset, name)  │ ← Class method
│ {class}                 │
│ + start(): void         │ ← Instance method
│ + stop(): void          │
└─────────────────────────┘
```

#### **Three Method Types Comparison**:
```python
class MyClass:
    def instance_method(self):
        """Access to instance (self) and class (self.__class__)"""
        print(f'Instance method bound to {self}')
        
    @classmethod
    def class_method(cls):
        """Access to class (cls) but not instance"""
        print(f'Class method bound to {cls}')
        
    @staticmethod
    def static_method():
        """No automatic binding - just a function in class namespace"""
        print('Static method not bound to anything')

# Usage examples
obj = MyClass()

# Instance method - needs instance
obj.instance_method()        # Instance method bound to <MyClass object>
# MyClass.instance_method()  # TypeError: missing 'self' argument

# Class method - can call from class or instance
MyClass.class_method()       # Class method bound to <class 'MyClass'>
obj.class_method()           # Class method bound to <class 'MyClass'>

# Static method - can call from class or instance, no binding
MyClass.static_method()      # Static method not bound to anything
obj.static_method()          # Static method not bound to anything
```

#### **Practical Example - Timer Class**:
```python
from datetime import datetime, timezone, timedelta

class Timer:
    tz = timezone.utc  # Class variable
    
    def __init__(self):
        self._started = None
        self._ended = None
    
    @staticmethod
    def current_dt_utc():
        """Get current UTC time - utility function"""
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        """Set timezone for all Timer instances"""
        cls.tz = timezone(timedelta(hours=offset), name)
    
    @classmethod
    def current_dt_tz(cls):
        """Get current time in class timezone"""
        return datetime.now(cls.tz)
    
    def start(self):
        """Start timing - instance method"""
        self._started = self.current_dt_tz()
        self._ended = None
    
    def stop(self):
        """Stop timing - instance method"""
        if self._started is None:
            raise ValueError('Timer not started')
        self._ended = self.current_dt_tz()
    
    @property
    def elapsed(self):
        """Get elapsed time"""
        if self._started is None:
            return None
        if self._ended is None:
            return self.current_dt_tz() - self._started
        return self._ended - self._started

# Usage
Timer.set_tz(-8, 'PST')     # Set timezone for all instances

t1 = Timer()
t2 = Timer()
print(t1.tz, t2.tz)         # Both show PST timezone

print(Timer.current_dt_utc())    # Static method - UTC time
print(Timer.current_dt_tz())     # Class method - PST time

t1.start()
# ... do some work ...
t1.stop()
print(t1.elapsed)               # Instance method usage
```

#### **When to Use Each Method Type**:

**Instance Methods**:
- Need access to instance data (`self`)
- Most common type of method
- Default choice for object behavior

**Class Methods**:
- Alternative constructors
- Operations on class data
- Factory methods
- When you need access to the class but not instance

**Static Methods**:
- Utility functions related to the class
- No need for instance or class data
- Could be a regular function, but logically belongs to the class
- Namespace organization

---

### **Notebook 14: Class Body Scope** 🔍

**Core Concept**: Understanding how scoping works within class definitions and potential pitfalls.

#### **Class Body Scope Rules**:
```
Class Body Scope:
┌─────────────────────┐
│   Global Scope      │
│  ┌───────────────┐  │
│  │ Class Scope   │  │ ← Class attributes live here
│  │               │  │
│  │ def method(): │  │ ← Methods defined here but...
│  │   # code      │  │
│  └───────────────┘  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Method Scope       │ ← ...methods execute in this scope
│  (nested in global, │   (NOT nested in class scope!)
│   NOT in class)     │
└─────────────────────┘
```

#### **Correct Class Scope Usage**:
```python
class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    # Can reference other class attributes in class body
    FULL = '{}.{}.{}'.format(MAJOR, MINOR, REVISION)

print(Language.FULL)    # '3.7.4'
```

#### **Scope Pitfall Example**:
```python
class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    
    @classmethod
    def cls_version(cls):
        # ❌ WRONG: Can't directly reference class attributes
        # return '{}.{}.{}'.format(MAJOR, MINOR, REVISION)
        
        # ✅ CORRECT: Must reference through cls or class name
        return '{}.{}.{}'.format(cls.MAJOR, cls.MINOR, cls.REVISION)
    
    @staticmethod
    def static_version():
        # ✅ CORRECT: Reference through class name
        return '{}.{}.{}'.format(Language.MAJOR, Language.MINOR, Language.REVISION)
    
    @property
    def version(self):
        # ✅ CORRECT: Reference through self (instance)
        return '{}.{}.{}'.format(self.MAJOR, self.MINOR, self.REVISION)
```

#### **Dangerous Scoping Example**:
```python
# Global variables
MAJOR = 0
MINOR = 0
REVISION = 1

class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    
    @classmethod
    def cls_version(cls):
        # ❌ DANGER: This picks up global variables!
        return '{}.{}.{}'.format(MAJOR, MINOR, REVISION)

print(Language.cls_version())  # '0.0.1' (not '3.7.4'!)
```

#### **Best Practices**:
- Always reference class attributes through `cls` or `self`
- Never rely on bare names in methods to reference class attributes
- Use class name for static methods: `ClassName.ATTRIBUTE`
- Be aware that method scope is NOT nested in class scope

---

## 🧠 Key Insights & Patterns

### **The Three Namespaces**
```python
class MyClass:
    class_attr = "shared"
    
    def __init__(self):
        self.instance_attr = "unique"

# 1. Class namespace
print(MyClass.__dict__)     # Contains class_attr, methods

# 2. Instance namespace  
obj = MyClass()
print(obj.__dict__)         # Contains instance_attr

# 3. Global namespace
print(globals().keys())     # Contains MyClass, other global symbols
```

### **Attribute Lookup Chain**
```
obj.attr lookup order:
1. obj.__dict__['attr']         (instance attribute)
2. type(obj).__dict__['attr']   (class attribute)  
3. parent_class.__dict__['attr'] (inheritance chain)
4. AttributeError
```

### **Property vs Attribute Decision Tree**
```
Do you need validation/computation?
├─ Yes: Use @property
└─ No: Use simple attribute
    ├─ Shared by all instances? → Class attribute
    └─ Unique per instance? → Instance attribute
```

---

## 🔍 UML Quick Reference

### **Class Diagram Elements**:
```
┌─────────────────────────┐
│      ClassName          │
├─────────────────────────┤ ← Attributes section
│ + public_attr: type     │
│ - private_attr: type    │
│ # protected_attr: type  │
├─────────────────────────┤ ← Methods section
│ + public_method(): type │
│ - private_method(): type│
│ {static} static_method()│
│ {class} class_method()  │
└─────────────────────────┘
```

### **Relationships**:
- **Association**: `───▶` (uses)
- **Inheritance**: `──△` (is-a)
- **Composition**: `──◆` (owns)
- **Dependency**: `┄▶` (depends on)

---

## 🎨 Complete UML Class Diagram Guide

### **1. Class Structure & Notation**

#### **Basic Class Box**:
```
┌─────────────────────────┐
│     <<stereotype>>      │ ← Optional stereotype
│      ClassName          │ ← Class name (required)
├─────────────────────────┤
│ - attribute1: type      │ ← Attributes section
│ + attribute2: type = val│   (with default values)
│ # attribute3: type      │
│ {readOnly} constant     │ ← Properties/constraints
├─────────────────────────┤
│ + method1(): returnType │ ← Methods section
│ - method2(param): void  │   (with parameters)
│ {abstract} method3()    │ ← Abstract methods
│ {static} method4()      │ ← Static methods
│ {class} method5()       │ ← Class methods
└─────────────────────────┘
```

#### **Access Modifiers**:
- **`+`** = **Public** (accessible from anywhere)
- **`-`** = **Private** (accessible only within the class)
- **`#`** = **Protected** (accessible within class and subclasses)
- **`~`** = **Package** (accessible within the same package/module)

#### **Method Stereotypes**:
- **`{static}`** = Static method (no self/cls parameter)
- **`{class}`** = Class method (receives cls parameter)
- **`{abstract}`** = Abstract method (must be implemented by subclasses)
- **`{readonly}`** = Read-only property

### **2. Relationships & Multiplicities**

#### **Association** (Uses/Has relationship):
```
┌─────────────┐     1    uses    0..*   ┌─────────────┐
│   Driver    │ ────────────────────────▶│     Car     │
└─────────────┘                          └─────────────┘
```

#### **Aggregation** (Has-a, but parts can exist independently):
```
┌─────────────┐     1   ◇────────────  *  ┌─────────────┐
│ University  │ ─────────────────────────▶│  Student    │
└─────────────┘     has                   └─────────────┘
```

#### **Composition** (Owns-a, parts cannot exist without whole):
```
┌─────────────┐     1   ◆────────────  *  ┌─────────────┐
│    House    │ ─────────────────────────▶│    Room     │
└─────────────┘     owns                  └─────────────┘
```

#### **Inheritance** (Is-a relationship):
```
┌─────────────┐
│   Animal    │ ← Parent/Base class
└─────────────┘
       △
       │ inherits
┌─────────────┐
│     Dog     │ ← Child/Derived class
└─────────────┘
```

#### **Dependency** (Uses temporarily):
```
┌─────────────┐                    ┌─────────────┐
│   Client    │ ┄┄┄┄┄┄┄┄depends┄┄▶│   Service   │
└─────────────┘                    └─────────────┘
```

### **3. Multiplicities & Cardinalities**

#### **Common Multiplicity Notations**:
- **`1`** = Exactly one
- **`0..1`** = Zero or one (optional)
- **`*`** or **`0..*`** = Zero or many
- **`1..*`** = One or many (at least one)
- **`2..5`** = Between 2 and 5
- **`3`** = Exactly 3

#### **Practical Example - Library System**:
```
┌─────────────────────────┐     1    manages    1..*  ┌─────────────────────────┐
│      Librarian          │ ─────────────────────────▶│        Book             │
├─────────────────────────┤                           ├─────────────────────────┤
│ + name: str             │                           │ + title: str            │
│ + employee_id: str      │                           │ + isbn: str             │
├─────────────────────────┤                           │ + available: bool       │
│ + check_out_book()      │                           ├─────────────────────────┤
│ + check_in_book()       │                           │ + get_info(): str       │
└─────────────────────────┘                           │ + mark_available()      │
                                                      └─────────────────────────┘
            │                                                    △
            │ 1                                                  │
            │                                                    │ 0..*
            ▼ 0..*                                               │
┌─────────────────────────┐     0..1   borrows    *             │
│       Member            │ ─────────────────────────┬──────────┘
├─────────────────────────┤                          │
│ + name: str             │                          │
│ + member_id: str        │                          │
│ + books_borrowed: int   │                          │
├─────────────────────────┤                          │
│ + borrow_book()         │                          │
│ + return_book()         │                          │
└─────────────────────────┘                          │
                                                     ▼
                                              ┌─────────────────────────┐
                                              │       TextBook          │
                                              ├─────────────────────────┤
                                              │ + subject: str          │
                                              │ + edition: int          │
                                              ├─────────────────────────┤
                                              │ + get_edition_info()    │
                                              └─────────────────────────┘
```

### **4. Advanced UML Features**

#### **Abstract Classes**:
```
┌─────────────────────────┐
│    <<abstract>>         │
│       Shape             │
├─────────────────────────┤
│ # color: str            │
├─────────────────────────┤
│ + get_color(): str      │
│ {abstract} + area(): float │ ← Must be implemented
│ {abstract} + perimeter(): float │
└─────────────────────────┘
```

#### **Interface (Python Protocol)**:
```
┌─────────────────────────┐
│    <<interface>>        │
│      Drawable           │
├─────────────────────────┤
│                         │
├─────────────────────────┤
│ {abstract} + draw()     │
│ {abstract} + erase()    │
└─────────────────────────┘
```

#### **Class with Properties**:
```
┌─────────────────────────┐
│       Circle            │
├─────────────────────────┤
│ - _radius: float        │ ← Private storage
├─────────────────────────┤
│ + radius: float         │ ← Property (getter/setter)
│ {property}              │
│ + area: float           │ ← Read-only property
│ {readonly property}     │
│ + circumference: float  │
│ {readonly property}     │
└─────────────────────────┘
```

### **5. Real-World Python Example with Full UML**

#### **Banking System Class Diagram**:
```
                    ┌─────────────────────────┐
                    │       <<abstract>>      │
                    │        Account          │
                    ├─────────────────────────┤
                    │ # _balance: float       │
                    │ # _account_number: str  │
                    │ # _owner: str           │
                    ├─────────────────────────┤
                    │ + balance: float        │
                    │ {readonly property}     │
                    │ + deposit(amount): void │
                    │ {abstract} withdraw()   │
                    │ + get_statement(): str  │
                    └─────────────────────────┘
                              △
                              │
              ┌───────────────┴────────────────┐
              │                                │
┌─────────────────────────┐        ┌─────────────────────────┐
│    CheckingAccount      │        │     SavingsAccount      │
├─────────────────────────┤        ├─────────────────────────┤
│ + overdraft_limit: float│        │ + interest_rate: float  │
├─────────────────────────┤        ├─────────────────────────┤
│ + withdraw(amount): void│        │ + withdraw(amount): void│
│ + charge_overdraft(): void│      │ + calculate_interest(): float│
└─────────────────────────┘        └─────────────────────────┘
              │                                │
              │ 1                              │ 1
              │                                │
              ▼ 1..*                           ▼ 0..*
┌─────────────────────────┐        ┌─────────────────────────┐
│      Customer           │◆───────│      Transaction       │
├─────────────────────────┤   1  * ├─────────────────────────┤
│ + name: str             │        │ + amount: float         │
│ + customer_id: str      │        │ + timestamp: datetime   │
│ + accounts: List[Account]│       │ + transaction_type: str │
├─────────────────────────┤        ├─────────────────────────┤
│ + add_account(): void   │        │ + execute(): void       │
│ + get_total_balance()   │        │ + get_details(): str    │
│ + get_all_accounts()    │        └─────────────────────────┘
└─────────────────────────┘
```

### **6. UML Best Practices**

#### **When to Use Different Relationships**:

1. **Inheritance (△)**: "Is-a" relationship
   ```python
   class Dog(Animal):  # Dog IS-A Animal
   ```

2. **Composition (◆)**: "Part-of" relationship, strong ownership
   ```python
   class House:
       def __init__(self):
           self.rooms = [Room(), Room()]  # Rooms are PART-OF House
   ```

3. **Aggregation (◇)**: "Has-a" relationship, weak ownership
   ```python
   class Team:
       def __init__(self, players):
           self.players = players  # Team HAS Players (but players exist independently)
   ```

4. **Association (→)**: "Uses" relationship
   ```python
   class Driver:
       def drive(self, car):  # Driver USES Car
           car.start()
   ```

#### **Common UML Mistakes to Avoid**:
- ❌ **Too much detail**: Don't include every single attribute/method
- ❌ **Wrong relationships**: Using composition when it should be aggregation
- ❌ **Missing multiplicities**: Always specify cardinalities
- ❌ **Inconsistent notation**: Pick one style and stick to it
- ❌ **Implementation details**: Focus on design, not code specifics

#### **UML Documentation Tips**:
1. **Start simple**: Begin with main classes and relationships
2. **Add detail gradually**: Start with class names, then add key attributes/methods
3. **Use meaningful names**: Class and method names should be self-explanatory
4. **Group related classes**: Use packages or namespaces for organization
5. **Validate with code**: Ensure your UML matches your implementation

---

## 📊 Progress Tracker

### **Notebook Completion**
- [x] **01 - Objects and Classes** ✅
  - [x] Read/watched material
  - [x] Created personal examples  
  - [x] UML diagrams created
  - [x] Understood core concepts

- [x] **02 - Class Attributes** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **03 - Callable Class Attributes** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **04 - Classes are Callable** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **05 - Data Attributes** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **06 - Function Attributes** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **07 - Initializing Class Instances** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **08 - Creating Attributes at Run-Time** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **09 - Properties** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **10 - Property Decorators** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **11 - Read-Only and Computed Properties** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **12 - Deleting Properties** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **13 - Class and Static Methods** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

- [x] **14 - Class Body Scope** ✅
  - [x] Read/watched material
  - [x] Completed exercises
  - [x] Created personal examples
  - [x] Understood core concepts

### **Overall Section Status**
- [x] **Foundation concepts mastered**
- [x] **Can implement class hierarchies confidently**  
- [x] **Understand when to use different attribute types**
- [x] **Property patterns mastered**
- [x] **Method types understood**
- [x] **UML basics learned**
- [x] **Ready for Section 4 (Polymorphism)**

---

**Started**: [Date]
**Completed**: [Date]  
**Time Invested**: [Hours]
**Difficulty Rating**: [4/5]
**Confidence Level**: [5/5]
**UML Comfort**: [4/5]

**Next Up**: Section 4 - Polymorphism and Special Methods

---

## 🎯 Section Summary

This section covered the **fundamental building blocks** of Python OOP:

1. **Object Model**: Everything is an object, classes are blueprints
2. **Namespaces**: Class vs instance attribute storage and lookup
3. **Methods**: How functions become bound methods
4. **Properties**: Controlled attribute access with validation/computation
5. **Method Types**: Instance, class, and static methods
6. **Scope**: Understanding class body scope and potential pitfalls

**Key Takeaway**: Python's object model is **simple but powerful** - understanding namespaces, attribute lookup, and the descriptor protocol (properties) gives you the foundation for all advanced OOP concepts. 