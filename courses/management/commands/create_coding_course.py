from django.core.management.base import BaseCommand
from courses.models import Subject, Course, Lesson, Quiz, Question, Choice
from django.utils import translation


class Command(BaseCommand):
    help = 'Create Introduction to Coding course with comprehensive lessons'

    def handle(self, *args, **options):
        # Get or create Computer Science subject for Class 11 (English)
        try:
            subject = Subject.objects.get(
                name='Computer Science',
                grade_level=11,
                language='en'
            )
        except Subject.DoesNotExist:
            subject = Subject.objects.create(
                name='Computer Science',
                description='Computer Science and Programming Fundamentals',
                grade_level=11,
                language='en'
            )
            self.stdout.write(f'Created subject: {subject}')

        # Create the Introduction to Coding course
        course, created = Course.objects.get_or_create(
            subject=subject,
            title='Introduction to Coding',
            defaults={
                'description': 'Learn the fundamentals of programming with Python. Perfect for beginners who want to start their coding journey.',
                'difficulty_level': 'beginner',
                'points_available': 500,
                'is_offline_available': True,
            }
        )

        if created:
            self.stdout.write(f'Created course: {course.title}')
        else:
            self.stdout.write(f'Course already exists: {course.title}')

        # Define lessons for the coding course
        lessons_data = [
            {
                'order': 1,
                'title': 'What is Programming?',
                'content': '''
# What is Programming?

Programming is the process of creating instructions for computers to follow. Just like you give instructions to a friend, programmers write code to tell computers what to do.

## Why Learn Programming?

1. **Problem Solving**: Programming teaches you to break down complex problems into smaller, manageable parts
2. **Creativity**: You can build websites, games, apps, and more
3. **Career Opportunities**: High demand for programmers in tech industry
4. **Logical Thinking**: Improves your analytical skills

## Types of Programming Languages

- **Python**: Great for beginners, used in data science and web development
- **JavaScript**: Used for web development
- **Java**: Used for mobile apps and enterprise software
- **C++**: Used for system programming and games

## Your First Program

Let's start with a simple "Hello World" program in Python:

```python
print("Hello, World!")
```

This program tells the computer to display "Hello, World!" on the screen.

## Key Concepts

- **Code**: Instructions written in a programming language
- **Program**: A complete set of instructions that performs a task
- **Algorithm**: A step-by-step procedure to solve a problem
- **Debugging**: Finding and fixing errors in code
                ''',
                'estimated_time': 15,
                'points': 25
            },
            {
                'order': 2,
                'title': 'Python Basics - Variables and Data Types',
                'content': '''
# Python Basics - Variables and Data Types

## What are Variables?

Variables are like containers that store information. Think of them as labeled boxes where you can put different things.

## Creating Variables

In Python, you create variables by giving them a name and assigning a value:

```python
# String (text)
name = "Alice"
age = 25
height = 5.6
is_student = True
```

## Data Types in Python

### 1. Strings (Text)
```python
name = "Alice"
message = 'Hello, World!'
```

### 2. Numbers
```python
# Integers (whole numbers)
age = 25
count = 100

# Floats (decimal numbers)
height = 5.6
price = 19.99
```

### 3. Booleans (True/False)
```python
is_student = True
is_working = False
```

## Working with Variables

```python
# Assigning values
x = 10
y = 20

# Using variables in calculations
sum = x + y
print(sum)  # Output: 30

# Updating variables
x = x + 5
print(x)  # Output: 15
```

## Practice Exercise

Create variables for:
- Your name (string)
- Your age (number)
- Whether you like programming (boolean)

```python
# Your code here
my_name = "Your Name"
my_age = 20
like_programming = True
```
                ''',
                'estimated_time': 20,
                'points': 30
            },
            {
                'order': 3,
                'title': 'Input and Output',
                'content': '''
# Input and Output in Python

## Output - Displaying Information

The `print()` function displays text on the screen:

```python
print("Hello, World!")
print("My name is Alice")
print("I am", 25, "years old")
```

## Input - Getting Information from User

The `input()` function gets text from the user:

```python
name = input("What is your name? ")
print("Hello,", name)
```

## Combining Input and Output

```python
# Get user's name
name = input("Enter your name: ")

# Get user's age
age = input("Enter your age: ")

# Display a message
print("Hello", name, "! You are", age, "years old.")
```

## Converting Input Types

By default, `input()` returns a string. To use numbers, convert them:

```python
# Get age as string, then convert to number
age_str = input("Enter your age: ")
age = int(age_str)  # Convert to integer

# Or do it in one line
age = int(input("Enter your age: "))
```

## Example Program

```python
# Simple calculator
print("Simple Calculator")
print("================")

# Get two numbers from user
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

# Calculate and display result
result = num1 + num2
print("The sum is:", result)
```

## Practice Exercise

Create a program that:
1. Asks for the user's name
2. Asks for their favorite color
3. Displays a personalized message

```python
# Your code here
name = input("What's your name? ")
color = input("What's your favorite color? ")
print("Hi", name, "! I see you like", color, "!")
```
                ''',
                'estimated_time': 25,
                'points': 35
            },
            {
                'order': 4,
                'title': 'Conditional Statements (if/else)',
                'content': '''
# Conditional Statements - Making Decisions

## What are Conditional Statements?

Conditional statements help your program make decisions based on different conditions. It's like saying "if this happens, then do that."

## Basic if Statement

```python
age = 18

if age >= 18:
    print("You are an adult")
```

## if-else Statement

```python
age = 16

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

## if-elif-else Statement

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

## Comparison Operators

- `==` : Equal to
- `!=` : Not equal to
- `>` : Greater than
- `<` : Less than
- `>=` : Greater than or equal to
- `<=` : Less than or equal to

## Logical Operators

- `and` : Both conditions must be true
- `or` : At least one condition must be true
- `not` : Reverses the condition

```python
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive")
else:
    print("You cannot drive")
```

## Example Program

```python
# Weather recommendation
temperature = int(input("What's the temperature? "))

if temperature > 30:
    print("It's hot! Wear light clothes and drink water.")
elif temperature > 20:
    print("Nice weather! Perfect for outdoor activities.")
elif temperature > 10:
    print("It's cool. Wear a jacket.")
else:
    print("It's cold! Bundle up and stay warm.")
```

## Practice Exercise

Create a program that determines if a number is positive, negative, or zero:

```python
# Your code here
number = int(input("Enter a number: "))

if number > 0:
    print("Positive number")
elif number < 0:
    print("Negative number")
else:
    print("Zero")
```
                ''',
                'estimated_time': 30,
                'points': 40
            },
            {
                'order': 5,
                'title': 'Loops - Repeating Actions',
                'content': '''
# Loops - Repeating Actions

## What are Loops?

Loops allow you to repeat a block of code multiple times. This is very useful when you need to do the same thing over and over.

## for Loop

The `for` loop repeats a block of code a specific number of times:

```python
# Count from 1 to 5
for i in range(1, 6):
    print(i)
```

## range() Function

`range()` generates a sequence of numbers:

```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8
```

## while Loop

The `while` loop repeats as long as a condition is true:

```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
```

## Looping through Lists

```python
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print("I like", fruit)
```

## Nested Loops

You can put loops inside other loops:

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(i, "x", j, "=", i * j)
```

## Loop Control

- `break`: Exit the loop immediately
- `continue`: Skip the rest of the current iteration

```python
# Print numbers 1-10, but skip 5
for i in range(1, 11):
    if i == 5:
        continue
    print(i)
```

## Example Programs

### Countdown Timer
```python
countdown = 5
while countdown > 0:
    print(countdown)
    countdown = countdown - 1
print("Blast off!")
```

### Sum of Numbers
```python
total = 0
for i in range(1, 6):
    total = total + i
print("Sum:", total)
```

## Practice Exercise

Create a program that prints the multiplication table for 5:

```python
# Your code here
number = 5
for i in range(1, 11):
    print(number, "x", i, "=", number * i)
```
                ''',
                'estimated_time': 35,
                'points': 45
            },
            {
                'order': 6,
                'title': 'Functions - Reusable Code',
                'content': '''
# Functions - Reusable Code

## What are Functions?

Functions are reusable blocks of code that perform a specific task. They help you organize your code and avoid repetition.

## Creating Functions

Use the `def` keyword to create a function:

```python
def say_hello():
    print("Hello, World!")

# Call the function
say_hello()
```

## Functions with Parameters

Parameters are inputs that functions can receive:

```python
def greet(name):
    print("Hello,", name)

# Call the function with an argument
greet("Alice")
greet("Bob")
```

## Functions with Return Values

Functions can return values using the `return` statement:

```python
def add_numbers(a, b):
    result = a + b
    return result

# Use the returned value
sum = add_numbers(5, 3)
print("Sum:", sum)
```

## Multiple Parameters

```python
def calculate_area(length, width):
    area = length * width
    return area

# Calculate area of a rectangle
area = calculate_area(10, 5)
print("Area:", area)
```

## Default Parameters

You can provide default values for parameters:

```python
def greet(name, greeting="Hello"):
    print(greeting, name)

greet("Alice")           # Uses default greeting
greet("Bob", "Hi")       # Uses custom greeting
```

## Built-in Functions

Python has many built-in functions:

```python
# len() - get length
name = "Alice"
print(len(name))  # Output: 5

# max() and min() - find maximum and minimum
numbers = [1, 5, 3, 9, 2]
print(max(numbers))  # Output: 9
print(min(numbers))  # Output: 1

# abs() - absolute value
print(abs(-5))  # Output: 5
```

## Example Programs

### Temperature Converter
```python
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

# Convert temperature
temp_c = 25
temp_f = celsius_to_fahrenheit(temp_c)
print(temp_c, "°C =", temp_f, "°F")
```

### Simple Calculator
```python
def calculator(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Invalid operation"

# Use the calculator
result = calculator("add", 10, 5)
print("Result:", result)
```

## Practice Exercise

Create a function that checks if a number is even or odd:

```python
# Your code here
def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

# Test the function
print(is_even(4))   # Should return True
print(is_even(7))   # Should return False
```
                ''',
                'estimated_time': 40,
                'points': 50
            },
            {
                'order': 7,
                'title': 'Lists and Data Structures',
                'content': '''
# Lists and Data Structures

## What are Lists?

Lists are collections of items stored in a specific order. They're like shopping lists where you can add, remove, and access items.

## Creating Lists

```python
# Empty list
empty_list = []

# List with items
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]
```

## Accessing List Items

Use index numbers to access items (starting from 0):

```python
fruits = ["apple", "banana", "orange"]

print(fruits[0])  # apple
print(fruits[1])  # banana
print(fruits[2])  # orange
```

## Modifying Lists

### Adding Items
```python
fruits = ["apple", "banana"]
fruits.append("orange")        # Add to end
fruits.insert(1, "grape")     # Insert at position 1
print(fruits)  # ['apple', 'grape', 'banana', 'orange']
```

### Removing Items
```python
fruits = ["apple", "banana", "orange"]
fruits.remove("banana")       # Remove by value
del fruits[0]                 # Remove by index
print(fruits)  # ['orange']
```

## List Operations

```python
numbers = [1, 2, 3, 4, 5]

# Length
print(len(numbers))  # 5

# Check if item exists
print(3 in numbers)  # True

# Count occurrences
print(numbers.count(2))  # 1
```

## Slicing Lists

```python
numbers = [1, 2, 3, 4, 5]

print(numbers[1:4])    # [2, 3, 4]
print(numbers[:3])     # [1, 2, 3]
print(numbers[2:])     # [3, 4, 5]
```

## Looping through Lists

```python
fruits = ["apple", "banana", "orange"]

# Method 1: Using index
for i in range(len(fruits)):
    print(i, fruits[i])

# Method 2: Direct iteration
for fruit in fruits:
    print(fruit)
```

## List Methods

```python
numbers = [3, 1, 4, 1, 5]

numbers.sort()          # Sort in place
print(numbers)          # [1, 1, 3, 4, 5]

numbers.reverse()       # Reverse in place
print(numbers)          # [5, 4, 3, 1, 1]

numbers.clear()         # Remove all items
print(numbers)          # []
```

## Example Programs

### Shopping List Manager
```python
shopping_list = []

while True:
    print("\\nShopping List Manager")
    print("1. Add item")
    print("2. Remove item")
    print("3. View list")
    print("4. Exit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        item = input("Enter item: ")
        shopping_list.append(item)
        print("Item added!")
    
    elif choice == "2":
        if shopping_list:
            print("Current list:", shopping_list)
            item = input("Enter item to remove: ")
            if item in shopping_list:
                shopping_list.remove(item)
                print("Item removed!")
            else:
                print("Item not found!")
        else:
            print("List is empty!")
    
    elif choice == "3":
        if shopping_list:
            print("Shopping List:")
            for i, item in enumerate(shopping_list, 1):
                print(f"{i}. {item}")
        else:
            print("List is empty!")
    
    elif choice == "4":
        print("Goodbye!")
        break
    
    else:
        print("Invalid choice!")
```

## Practice Exercise

Create a program that finds the largest number in a list:

```python
# Your code here
def find_largest(numbers):
    largest = numbers[0]
    for number in numbers:
        if number > largest:
            largest = number
    return largest

# Test the function
numbers = [3, 7, 2, 9, 1]
print("Largest number:", find_largest(numbers))
```
                ''',
                'estimated_time': 45,
                'points': 55
            },
            {
                'order': 8,
                'title': 'Project - Build a Simple Calculator',
                'content': '''
# Project - Build a Simple Calculator

## Project Overview

Let's build a simple calculator that can perform basic arithmetic operations. This project will combine everything we've learned so far.

## Features

Our calculator will:
1. Display a menu of operations
2. Get two numbers from the user
3. Perform the selected operation
4. Display the result
5. Ask if the user wants to continue

## Step-by-Step Implementation

### Step 1: Display Menu
```python
def show_menu():
    print("\\n=== Simple Calculator ===")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
```

### Step 2: Get Numbers
```python
def get_numbers():
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        return num1, num2
    except ValueError:
        print("Invalid input! Please enter numbers only.")
        return None, None
```

### Step 3: Perform Operations
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        print("Error: Cannot divide by zero!")
        return None
```

### Step 4: Main Calculator Function
```python
def calculator():
    while True:
        show_menu()
        choice = input("Choose an operation (1-5): ")
        
        if choice == "5":
            print("Thank you for using the calculator!")
            break
        
        elif choice in ["1", "2", "3", "4"]:
            num1, num2 = get_numbers()
            
            if num1 is not None and num2 is not None:
                if choice == "1":
                    result = add(num1, num2)
                    print(f"{num1} + {num2} = {result}")
                
                elif choice == "2":
                    result = subtract(num1, num2)
                    print(f"{num1} - {num2} = {result}")
                
                elif choice == "3":
                    result = multiply(num1, num2)
                    print(f"{num1} × {num2} = {result}")
                
                elif choice == "4":
                    result = divide(num1, num2)
                    if result is not None:
                        print(f"{num1} ÷ {num2} = {result}")
        else:
            print("Invalid choice! Please select 1-5.")
```

### Step 5: Run the Calculator
```python
# Start the calculator
calculator()
```

## Complete Program

```python
def show_menu():
    print("\\n=== Simple Calculator ===")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")

def get_numbers():
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        return num1, num2
    except ValueError:
        print("Invalid input! Please enter numbers only.")
        return None, None

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        print("Error: Cannot divide by zero!")
        return None

def calculator():
    print("Welcome to the Simple Calculator!")
    
    while True:
        show_menu()
        choice = input("Choose an operation (1-5): ")
        
        if choice == "5":
            print("Thank you for using the calculator!")
            break
        
        elif choice in ["1", "2", "3", "4"]:
            num1, num2 = get_numbers()
            
            if num1 is not None and num2 is not None:
                if choice == "1":
                    result = add(num1, num2)
                    print(f"{num1} + {num2} = {result}")
                
                elif choice == "2":
                    result = subtract(num1, num2)
                    print(f"{num1} - {num2} = {result}")
                
                elif choice == "3":
                    result = multiply(num1, num2)
                    print(f"{num1} × {num2} = {result}")
                
                elif choice == "4":
                    result = divide(num1, num2)
                    if result is not None:
                        print(f"{num1} ÷ {num2} = {result}")
        else:
            print("Invalid choice! Please select 1-5.")

# Start the calculator
calculator()
```

## Enhancements

Try adding these features:
1. **History**: Keep track of previous calculations
2. **Memory**: Store and recall numbers
3. **Advanced Operations**: Square root, power, percentage
4. **Better Error Handling**: Handle more types of errors
5. **GUI**: Create a graphical interface

## Practice Exercise

Create your own version of the calculator with additional features like:
- Square root calculation
- Power calculation (a^b)
- Percentage calculation

```python
# Your enhanced calculator here
```
                ''',
                'estimated_time': 50,
                'points': 60
            }
        ]

        # Create lessons
        created_lessons = 0
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                course=course,
                order=lesson_data['order'],
                defaults={
                    'title': lesson_data['title'],
                    'content': lesson_data['content'],
                    'estimated_time': lesson_data['estimated_time'],
                    'points': lesson_data['points'],
                }
            )
            if created:
                created_lessons += 1
                self.stdout.write(f'Created lesson: {lesson.title}')

        # Create a quiz for the course
        try:
            project_lesson = Lesson.objects.get(course=course, order=8)
            quiz, quiz_created = Quiz.objects.get_or_create(
                lesson=project_lesson,
                defaults={
                    'title': 'Introduction to Coding Quiz',
                    'description': 'Test your understanding of basic programming concepts',
                    'passing_score': 70,
                    'points': 20,
                }
            )
        except Lesson.DoesNotExist:
            self.stdout.write('Project lesson not found, skipping quiz creation')
            quiz_created = False

        if quiz_created:
            self.stdout.write(f'Created quiz: {quiz.title}')

            # Create quiz questions
            questions_data = [
                {
                    'question_text': 'What is the correct way to create a variable in Python?',
                    'choices': [
                        ('var name = "Alice"', False),
                        ('name = "Alice"', True),
                        ('name := "Alice"', False),
                        ('string name = "Alice"', False),
                    ]
                },
                {
                    'question_text': 'Which function is used to get input from the user?',
                    'choices': [
                        ('input()', True),
                        ('get_input()', False),
                        ('read()', False),
                        ('user_input()', False),
                    ]
                },
                {
                    'question_text': 'What will this code output: print(3 + 2 * 4)',
                    'choices': [
                        ('20', False),
                        ('11', True),
                        ('14', False),
                        ('Error', False),
                    ]
                },
                {
                    'question_text': 'Which loop is used when you know the exact number of iterations?',
                    'choices': [
                        ('while loop', False),
                        ('for loop', True),
                        ('if loop', False),
                        ('repeat loop', False),
                    ]
                },
                {
                    'question_text': 'What keyword is used to define a function in Python?',
                    'choices': [
                        ('function', False),
                        ('def', True),
                        ('create', False),
                        ('define', False),
                    ]
                }
            ]

            for q_data in questions_data:
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=q_data['question_text'],
                    points=2
                )

                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        is_correct=is_correct
                    )

            self.stdout.write(f'Created {len(questions_data)} quiz questions')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created Introduction to Coding course with {created_lessons} lessons and quiz!'
            )
        )
