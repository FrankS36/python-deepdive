## 🔗 Method Binding in Python

In Python, **methods are just functions** that get “bound” to objects or classes depending on how they’re defined and called. 

*Binding controls what the **first argument** (`self` or `cls`) represents.*

### 1. Instance Methods (Default)
- Defined with `def method(self, ...)`.
- Bound to an **object instance**.
- The first argument (`self`) refers to that object.

    class Dog:
        def bark(self):
            print(f"{self} says woof!")

    d = Dog()
    d.bark()      # Behind the scenes → Dog.bark(d)

---

### 2. Class Methods
- Decorated with `@classmethod`.
- Bound to the **class**, not an instance.
- First argument is `cls` (the class itself).

    class Dog:
        @classmethod
        def species(cls):
            print(f"This is a {cls.__name__}")

    Dog.species()   # works on class
    d = Dog()
    d.species()     # also works, still passes class

---

### 3. Static Methods
- Decorated with `@staticmethod`.
- **Not bound** to either class or instance.
- Behaves like a plain function placed inside a class for organization.

    class Math:
        @staticmethod
        def add(a, b):
            return a + b

    Math.add(2, 3)  # 5

---

### 4. Free Functions vs Bound Methods
- Accessing a method on a class returns the **unbound function**.
- Accessing a method on an instance returns a **bound method** (already packaged with `self`).

    print(Dog.bark)   # function object
    print(d.bark)     # bound method with self

---

**Summary:**  
- **Instance methods** bind to the object (`self`).  
- **Class methods** bind to the class (`cls`).  
- **Static methods** don’t bind at all.  
This flexibility is what makes Python’s OOP model highly dynamic.

## 🔗 Method Binding — Visual Diagram

Here’s a simple **mental model** for how Python binds methods:
```



+-------------------+       +-----------------------+
\|   Class: Dog      |       |   Instance: fido      |
\|-------------------|       |-----------------------|
\| def bark(self)    | <---> | fido.bark()           |
\| @classmethod      | <---> | fido.species()        |
\| def species(cls)  |       |                       |
\| @staticmethod     | <---> | fido.info()           |
\| def info()        |       |                       |
+-------------------+       +-----------------------+

```

---

### 1. Instance Method
```

Dog.bark(fido)   --->   fido.bark()
↑
(unbound function on class → bound to instance)

```
- Bound to **instance**.  
- First arg is `self`.

---

### 2. Class Method
```

Dog.species()    --->   fido.species()
↑
(bound to the class itself)

```
- Bound to **class**.  
- First arg is `cls`.

---

### 3. Static Method
```

Dog.info()       --->   fido.info()
(no binding – just a namespaced function)

```
- **Not bound** to anything.  
- Works the same from class or instance.

---

✅ **Visual Summary:**  
- **Instance method** → Object bound (`self`)  
- **Class method** → Class bound (`cls`)  
- **Static method** → No binding at all  

