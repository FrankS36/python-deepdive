class Program: 
    def __init__(self, language, version, author, release_date, license, license_url, license_text):
        # ✅ Actually use the parameters passed to the constructor
        self.language = language
        self.version = version
        self.author = author
        self.release_date = release_date
        self.license = license
        self.license_url = license_url
        self.license_text = license_text

print("=== CLASS ATTRIBUTES ===")
# View the attributes of the class itself
print("Class __dict__:", Program.__dict__)
print("Class name:", Program.__name__)
print("__init__ method:", Program.__init__)
print("Using getattr for __init__:", getattr(Program, '__init__'))

print("\n=== TRYING TO ACCESS INSTANCE ATTRIBUTES ON CLASS ===")
# ❌ These will fail because 'language' and 'version' are instance attributes
try:
    print("Class language:", getattr(Program, 'language'))
except AttributeError as e:
    print(f"Error: {e}")

try:
    print("Class version:", getattr(Program, 'version'))
except AttributeError as e:
    print(f"Error: {e}")

print("\n=== CREATING AN INSTANCE ===")
# ✅ Create an instance with actual values
python_program = Program(
    language="Python",
    version="3.10", 
    author="Guido van Rossum",
    release_date="2022-10-04",
    license="PSF",
    license_url="https://www.python.org/psf/license/",
    license_text="Python Software Foundation License"
)

print("\n=== INSTANCE ATTRIBUTES ===")
# ✅ Now we can access instance attributes
print("Instance __dict__:", python_program.__dict__)
print("Instance language:", python_program.language)
print("Instance version:", python_program.version)
print("Using getattr on instance:", getattr(python_program, 'language'))

print("\n=== DEMONSTRATION: DIFFERENT INSTANCES ===")
# Create another instance with different values
java_program = Program(
    language="Java",
    version="17",
    author="James Gosling", 
    release_date="2021-09-14",
    license="Oracle License",
    license_url="https://oracle.com/license",
    license_text="Oracle Technology License"
)

print("Python program language:", python_program.language)
print("Java program language:", java_program.language) 