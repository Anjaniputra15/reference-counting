# Python Reference Counting Demonstration

This program provides a comprehensive demonstration of Python's reference counting memory management system.

## What is Reference Counting?

Reference counting is Python's primary memory management mechanism where each object keeps track of how many references point to it. When the reference count drops to zero, Python automatically deallocates the object.

## Features

The demonstration includes:

1. **Basic Reference Counting** - Shows how reference counts change with different operations
2. **Circular References** - Demonstrates the limitation of reference counting
3. **Garbage Collection** - Shows how Python handles circular references
4. **Function Behavior** - Demonstrates reference counting in function calls
5. **Data Structures** - Shows how different containers affect reference counts
6. **Interactive Demo** - Allows you to control reference counting manually

## How to Run

```bash
python reference_counting_demo.py
```

Or use the simple runner:

```bash
python run_demo.py
```

## What You'll Learn

- How Python tracks object references
- When objects are created and destroyed
- How different operations affect reference counts
- Why circular references are problematic
- How garbage collection complements reference counting

## Example Output

```
🐍 PYTHON REFERENCE COUNTING DEMONSTRATION

🎯 BASIC REFERENCE COUNTING DEMONSTRATION
============================================================

1. Creating an object...
🔵 Created object 'my_object' (initial ref count: 1)
📊 'my_object' ref count: 1 (after creation)

2. Creating another reference...
📊 'my_object' ref count: 2 (after creating another reference)

3. Storing in a list...
📊 'my_object' ref count: 3 (after storing in list)

...

🔴 Object 'my_object' is being deallocated (ref count reached 0)
```

## Key Concepts Demonstrated

- **Reference Count Initialization**: Objects start with count = 1
- **Reference Increments**: Count increases with new references
- **Reference Decrements**: Count decreases when references are removed
- **Automatic Deallocation**: Objects freed when count reaches 0
- **Circular Reference Problem**: Objects that reference each other
- **Garbage Collection**: Python's solution to circular references

## Interactive Commands

When you run the interactive demo, you can use these commands:

- `create` - Create a new object
- `ref` - Create a new reference to current object
- `list` - Store object in a list
- `dict` - Store object in a dictionary
- `remove` - Remove last reference
- `status` - Show current reference count
- `quit` - Exit demo

## Requirements

- Python 3.6 or higher
- No additional packages required

## Understanding the Output

- 🔵 Blue circles indicate object creation
- 🔴 Red circles indicate object deallocation
- 📊 Shows current reference count
- 🎯 Different sections demonstrate various aspects of reference counting

This program will help you understand how Python manages memory and why certain objects behave the way they do in terms of when they're created and destroyed. 