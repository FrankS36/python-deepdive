# Section 2: Classes 🏗️

## 🎯 Learning Objectives
- [ ] Understand Python's object model and how classes work internally
- [ ] Master the difference between class and instance attributes
- [ ] Learn how method binding works in Python
- [ ] Implement properties for controlled attribute access
- [ ] Know when to use class methods, static methods, and instance methods
- [ ] Understand class body scope and namespace behavior

---

## 📖 Key Concepts

### 1. Objects and Classes (Notebook 01)
**Definition**: In Python, everything is an object, including classes themselves. Classes are blueprints for creating objects.

**Key Points**:
- Classes are objects of type `type`
- Instances are objects of the class type
- `id()`, `type()`, and `isinstance()` for object inspection

**When to use**: Understanding this helps with metaclassing and dynamic class creation later.

**Personal Notes**:
```python
# My example exploring object relationships
class MyClass:
    pass

obj = MyClass()
print(f"obj is instance of MyClass: {isinstance(obj, MyClass)}")
print(f"MyClass is instance of type: {isinstance(MyClass, type)}")
print(f"Type of obj: {type(obj)}")
print(f"Type of MyClass: {type(MyClass)}")
```

### 2. Class vs Instance Attributes (Notebook 02)
**Definition**: Class attributes are shared by all instances; instance attributes are unique to each instance.

**Key Points**:
- Class attributes defined in class body
- Instance attributes typically defined in `__init__`
- Attribute lookup order: instance → class → parent classes
- Modifying class attributes affects all instances

**When to use**:
- Class attributes: Constants, counters, shared configuration
- Instance attributes: Object-specific data

**Important Insight**: 🔍 
When you assign to an attribute on an instance, Python creates an instance attribute that shadows the class attribute for that instance only!

### 3. Properties (Notebooks 09-11)
**Definition**: Properties provide controlled access to attributes using getter/setter/deleter methods.

**Key Patterns**:
```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
```

**When to use**:
- Validation on attribute assignment
- Computed properties
- Backward compatibility when changing implementation
- Logging/debugging attribute access

---

## 💡 Important Insights

### 🧠 Aha Moments
1. **Class attributes are shared**: When I first learned that modifying a class attribute affects ALL instances, it clicked why we need to be careful with mutable defaults.

2. **Properties are descriptors**: Understanding that `@property` is just syntactic sugar for the descriptor protocol helped connect the dots to Section 8.

3. **Method binding magic**: Learning that `obj.method()` is actually `Class.method(obj)` under the hood explained so much about Python's object model.

### 🔗 Connections to Other Concepts
- **Section 8 (Descriptors)**: Properties are implemented using descriptors
- **Section 14 (Metaclasses)**: Understanding `type` as the metaclass for classes
- **Section 4 (Special Methods)**: `__init__` is just one of many special methods

---

## 🔍 Code Examples

### Example 1: Class vs Instance Attributes
```python
class Counter:
    # Class attribute - shared by all instances
    total_count = 0
    
    def __init__(self, name):
        # Instance attribute - unique to each instance
        self.name = name
        self.count = 0
        # Accessing class attribute through class
        Counter.total_count += 1
    
    def increment(self):
        self.count += 1
        Counter.total_count += 1

# Testing the behavior
c1 = Counter("First")
c2 = Counter("Second")
print(f"Total counters: {Counter.total_count}")  # 2

c1.increment()
c2.increment()
print(f"C1 count: {c1.count}")  # 1
print(f"C2 count: {c2.count}")  # 1
print(f"Total count: {Counter.total_count}")  # 4
```

### Example 2: Property with Validation
```python
class BankAccount:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount
    
    @property
    def balance_str(self):
        """Computed property - always calculated"""
        return f"${self._balance:.2f}"

# Usage
account = BankAccount(100)
print(account.balance_str)  # $100.00
account.balance = 200
print(account.balance_str)  # $200.00
```

### Example 3: Class and Static Methods
```python
class MathUtils:
    pi = 3.14159
    
    @classmethod
    def circle_area_from_radius(cls, radius):
        """Class method - has access to class attributes"""
        return cls.pi * radius ** 2
    
    @staticmethod
    def circle_area(radius, pi=3.14159):
        """Static method - independent utility function"""
        return pi * radius ** 2
    
    def instance_method(self):
        """Instance method - has access to instance"""
        return f"Instance method called on {self}"

# Usage demonstrates the differences
print(MathUtils.circle_area_from_radius(5))  # Uses class attribute
print(MathUtils.circle_area(5))  # Independent function
```

---

## ❓ Questions & Challenges

### 🤔 Things I'm Still Unclear About
- [ ] When exactly should I use `@classmethod` vs `@staticmethod`?
- [ ] How does property lookup work with inheritance?
- [ ] Performance implications of properties vs direct attribute access

### 🎯 Areas That Need More Practice
- [ ] Creating complex property hierarchies
- [ ] Understanding when class attributes vs instance attributes make sense
- [ ] Building effective class designs that use all these concepts together

### 🔍 Experiments to Try
- [ ] Create a class that uses all three method types appropriately
- [ ] Build a property that depends on other properties
- [ ] Investigate performance differences between properties and attributes

---

## 🔗 Related Concepts

### Cross-References
- **Descriptors (Section 8)**: Properties are implemented using the descriptor protocol
- **Inheritance (Section 6)**: How attribute lookup works with inheritance
- **Metaclasses (Section 14)**: How classes themselves are created and managed

### Connection to My Previous Learning
- This connects to my beginner OOP guide where I covered basic classes
- The property patterns here are more advanced than what I implemented before
- Understanding the object model helps explain the behavior I saw in my advanced guide

---

## 📊 Progress Tracker

### Notebook Completion
- [ ] **01 - Objects and Classes** 
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **02 - Class Attributes**
  - [ ] Read/watched material  
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **03 - Callable Class Attributes**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **04 - Classes are Callable**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **05 - Data Attributes**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **06 - Function Attributes**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **07 - Initializing Class Instances**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **08 - Creating Attributes at Run-Time**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **09 - Properties**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **10 - Property Decorators**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **11 - Read-Only and Computed Properties**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **12 - Deleting Properties**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **13 - Class and Static Methods**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

- [ ] **14 - Class Body Scope**
  - [ ] Read/watched material
  - [ ] Completed exercises
  - [ ] Created personal examples
  - [ ] Understood core concepts

### Overall Section Status
- [ ] **Foundation concepts mastered**
- [ ] **Can implement class hierarchies confidently**
- [ ] **Understand when to use different attribute types**
- [ ] **Ready for Section 4 (Polymorphism)**

---

**Started**: [Date]
**Completed**: [Date]
**Time Invested**: [Hours]
**Difficulty Rating**: [1-5]
**Confidence Level**: [1-5]

**Next Up**: Section 4 - Polymorphism and Special Methods 