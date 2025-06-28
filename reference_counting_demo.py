#!/usr/bin/env python3
"""
Reference Counting Demonstration Program
This program shows how Python manages memory using reference counting.
"""

import sys
import gc
import time
from typing import Any, Dict, List

class ReferenceTracker:
    """A class to track and display reference counts of objects."""
    
    def __init__(self, name: str):
        self.name = name
        self.ref_count = 0
        print(f"🔵 Created object '{name}' (initial ref count: 1)")
    
    def __del__(self):
        print(f"🔴 Object '{self.name}' is being deallocated (ref count reached 0)")
    
    def get_ref_count(self) -> int:
        """Get the current reference count of this object."""
        return sys.getrefcount(self) - 1  # Subtract 1 for the function parameter
    
    def show_status(self, context: str = ""):
        """Display the current reference count with context."""
        count = self.get_ref_count()
        print(f"📊 '{self.name}' ref count: {count} {context}")

def demonstrate_basic_reference_counting():
    """Demonstrate basic reference counting operations."""
    print("\n" + "="*60)
    print("🎯 BASIC REFERENCE COUNTING DEMONSTRATION")
    print("="*60)
    
    # Create an object
    print("\n1. Creating an object...")
    obj = ReferenceTracker("my_object")
    obj.show_status("(after creation)")
    
    # Create another reference
    print("\n2. Creating another reference...")
    another_ref = obj
    obj.show_status("(after creating another reference)")
    
    # Store in a list
    print("\n3. Storing in a list...")
    my_list = [obj]
    obj.show_status("(after storing in list)")
    
    # Store in a dictionary
    print("\n4. Storing in a dictionary...")
    my_dict = {"key": obj}
    obj.show_status("(after storing in dict)")
    
    # Pass to a function
    print("\n5. Passing to a function...")
    def dummy_function(param):
        param.show_status("(inside function)")
        return param
    
    result = dummy_function(obj)
    obj.show_status("(after function call)")
    
    # Remove references one by one
    print("\n6. Removing references one by one...")
    
    print("   Removing from dictionary...")
    del my_dict["key"]
    obj.show_status("(after removing from dict)")
    
    print("   Removing from list...")
    my_list.clear()
    obj.show_status("(after removing from list)")
    
    print("   Removing function result...")
    del result
    obj.show_status("(after removing function result)")
    
    print("   Removing second reference...")
    del another_ref
    obj.show_status("(after removing second reference)")
    
    print("   Removing original reference...")
    del obj
    print("   (Object should be deallocated now)")

def demonstrate_circular_references():
    """Demonstrate the circular reference problem."""
    print("\n" + "="*60)
    print("🔄 CIRCULAR REFERENCE DEMONSTRATION")
    print("="*60)
    
    class CircularNode:
        def __init__(self, name: str):
            self.name = name
            self.ref = None
            print(f"🔵 Created circular node '{name}'")
        
        def __del__(self):
            print(f"🔴 Circular node '{self.name}' is being deallocated")
    
    print("\n1. Creating circular reference...")
    node_a = CircularNode("A")
    node_b = CircularNode("B")
    
    # Create circular reference
    node_a.ref = node_b
    node_b.ref = node_a
    
    print(f"   Node A ref count: {sys.getrefcount(node_a) - 1}")
    print(f"   Node B ref count: {sys.getrefcount(node_b) - 1}")
    
    print("\n2. Removing direct references...")
    del node_a
    del node_b
    
    print("   Direct references removed, but objects still exist due to circular reference")
    print("   (Objects will be cleaned up by garbage collector)")

def demonstrate_garbage_collection():
    """Demonstrate garbage collection handling circular references."""
    print("\n" + "="*60)
    print("🗑️  GARBAGE COLLECTION DEMONSTRATION")
    print("="*60)
    
    class GarbageNode:
        def __init__(self, name: str):
            self.name = name
            self.ref = None
            print(f"🔵 Created garbage node '{name}'")
        
        def __del__(self):
            print(f"🔴 Garbage node '{self.name}' is being deallocated")
    
    print("\n1. Creating circular references...")
    nodes = []
    for i in range(3):
        node = GarbageNode(f"Node_{i}")
        nodes.append(node)
    
    # Create circular references
    nodes[0].ref = nodes[1]
    nodes[1].ref = nodes[2]
    nodes[2].ref = nodes[0]
    
    print(f"   Created {len(nodes)} nodes with circular references")
    
    print("\n2. Removing direct references...")
    del nodes
    
    print("3. Running garbage collection...")
    collected = gc.collect()
    print(f"   Garbage collector collected {collected} objects")

def demonstrate_reference_counting_in_functions():
    """Demonstrate reference counting behavior in functions."""
    print("\n" + "="*60)
    print("⚙️  FUNCTION REFERENCE COUNTING DEMONSTRATION")
    print("="*60)
    
    def function_with_local_ref():
        print("   Entering function...")
        local_obj = ReferenceTracker("function_local")
        local_obj.show_status("(inside function)")
        print("   Exiting function...")
        # local_obj goes out of scope here
    
    def function_with_return():
        print("   Entering function with return...")
        local_obj = ReferenceTracker("function_return")
        local_obj.show_status("(inside function)")
        print("   Returning object...")
        return local_obj
    
    print("\n1. Function with local object (no return):")
    function_with_local_ref()
    print("   (Object should be deallocated when function exits)")
    
    print("\n2. Function with returned object:")
    returned_obj = function_with_return()
    returned_obj.show_status("(after function return)")
    
    print("\n3. Removing returned object:")
    del returned_obj
    print("   (Object should be deallocated now)")

def demonstrate_data_structures():
    """Demonstrate reference counting with various data structures."""
    print("\n" + "="*60)
    print("📦 DATA STRUCTURES REFERENCE COUNTING")
    print("="*60)
    
    # Create objects
    obj1 = ReferenceTracker("list_object")
    obj2 = ReferenceTracker("dict_object")
    obj3 = ReferenceTracker("set_object")
    
    print("\n1. Storing objects in different data structures:")
    
    # List
    my_list = [obj1]
    obj1.show_status("(in list)")
    
    # Dictionary
    my_dict = {"key": obj2}
    obj2.show_status("(in dict)")
    
    # Set
    my_set = {obj3}
    obj3.show_status("(in set)")
    
    # Tuple
    my_tuple = (obj1, obj2, obj3)
    obj1.show_status("(in tuple)")
    obj2.show_status("(in tuple)")
    obj3.show_status("(in tuple)")
    
    print("\n2. Removing from data structures:")
    
    # Remove from list
    my_list.clear()
    obj1.show_status("(removed from list)")
    
    # Remove from dict
    del my_dict["key"]
    obj2.show_status("(removed from dict)")
    
    # Remove from set
    my_set.clear()
    obj3.show_status("(removed from set)")
    
    print("\n3. Removing tuple reference:")
    del my_tuple
    print("   (Objects should be deallocated now)")

def interactive_demo():
    """Interactive demonstration where user can control reference counting."""
    print("\n" + "="*60)
    print("🎮 INTERACTIVE REFERENCE COUNTING DEMO")
    print("="*60)
    
    print("\nThis demo lets you control reference counting interactively.")
    print("Commands:")
    print("  'create' - Create a new object")
    print("  'ref' - Create a new reference to current object")
    print("  'list' - Store object in a list")
    print("  'dict' - Store object in a dictionary")
    print("  'remove' - Remove last reference")
    print("  'status' - Show current reference count")
    print("  'quit' - Exit demo")
    
    current_obj = None
    references = []
    
    while True:
        command = input("\nEnter command: ").strip().lower()
        
        if command == 'quit':
            break
        elif command == 'create':
            current_obj = ReferenceTracker("interactive_object")
            references = [current_obj]
            print("✅ Object created!")
        elif command == 'ref':
            if current_obj:
                references.append(current_obj)
                current_obj.show_status("(new reference created)")
            else:
                print("❌ No object to reference. Create one first.")
        elif command == 'list':
            if current_obj:
                references.append([current_obj])
                current_obj.show_status("(stored in list)")
            else:
                print("❌ No object to store. Create one first.")
        elif command == 'dict':
            if current_obj:
                references.append({"key": current_obj})
                current_obj.show_status("(stored in dict)")
            else:
                print("❌ No object to store. Create one first.")
        elif command == 'remove':
            if references:
                removed = references.pop()
                if current_obj:
                    current_obj.show_status("(reference removed)")
            else:
                print("❌ No references to remove.")
        elif command == 'status':
            if current_obj:
                current_obj.show_status("(current status)")
            else:
                print("❌ No object exists.")
        else:
            print("❌ Unknown command. Try 'create', 'ref', 'list', 'dict', 'remove', 'status', or 'quit'.")

def main():
    """Main function to run all demonstrations."""
    print("🐍 PYTHON REFERENCE COUNTING DEMONSTRATION")
    print("This program shows how Python manages memory using reference counting.")
    
    try:
        # Run all demonstrations
        demonstrate_basic_reference_counting()
        demonstrate_circular_references()
        demonstrate_garbage_collection()
        demonstrate_reference_counting_in_functions()
        demonstrate_data_structures()
        
        # Ask if user wants interactive demo
        response = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
        
        print("\n" + "="*60)
        print("✅ DEMONSTRATION COMPLETE!")
        print("="*60)
        print("\nKey takeaways:")
        print("• Objects are created with reference count = 1")
        print("• Reference count increases when new references are created")
        print("• Reference count decreases when references are removed")
        print("• Objects are deallocated when reference count reaches 0")
        print("• Circular references require garbage collection to clean up")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")

if __name__ == "__main__":
    main() 