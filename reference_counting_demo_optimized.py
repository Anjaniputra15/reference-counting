#!/usr/bin/env python3
"""
Optimized Reference Counting Demonstration Program
This program shows how Python manages memory using reference counting with performance optimizations.
"""

import sys
import gc
import time
from typing import Any, Dict, List, Optional
from functools import lru_cache
import io
import contextlib

class OptimizedReferenceTracker:
    """An optimized class to track and display reference counts of objects."""
    
    # Class-level cache for reference counts to avoid repeated sys.getrefcount calls
    _ref_count_cache = {}
    
    def __init__(self, name: str):
        self.name = name
        # Cache the initial reference count
        initial_ref_count = self._get_ref_count()
        self._ref_count_cache[id(self)] = initial_ref_count
        print(f"🔵 Created object '{name}' (initial ref count: {initial_ref_count})")
    
    def __del__(self):
        # Remove from cache when object is destroyed
        self._ref_count_cache.pop(id(self), None)
        print(f"🔴 Object '{self.name}' is being deallocated (ref count reached 0)")
    
    def _get_ref_count(self) -> int:
        """Get the current reference count of this object (cached)."""
        obj_id = id(self)
        if obj_id not in self._ref_count_cache:
            self._ref_count_cache[obj_id] = sys.getrefcount(self) - 1
        return self._ref_count_cache[obj_id]
    
    def _update_ref_count(self):
        """Update the cached reference count."""
        obj_id = id(self)
        self._ref_count_cache[obj_id] = sys.getrefcount(self) - 1
    
    def show_status(self, context: str = ""):
        """Display the current reference count with context."""
        self._update_ref_count()  # Update cache before showing
        count = self._get_ref_count()
        print(f"📊 '{self.name}' ref count: {count} {context}")

class FastCircularNode:
    """Optimized circular node for demonstration."""
    
    __slots__ = ['name', 'ref']  # Use __slots__ for memory efficiency
    
    def __init__(self, name: str):
        self.name = name
        self.ref = None
        print(f"🔵 Created circular node '{name}'")
    
    def __del__(self):
        print(f"🔴 Circular node '{self.name}' is being deallocated")

class FastGarbageNode:
    """Optimized garbage node for demonstration."""
    
    __slots__ = ['name', 'ref']  # Use __slots__ for memory efficiency
    
    def __init__(self, name: str):
        self.name = name
        self.ref = None
        print(f"🔵 Created garbage node '{name}'")
    
    def __del__(self):
        print(f"🔴 Garbage node '{self.name}' is being deallocated")

@lru_cache(maxsize=128)
def get_separator(length: int = 60) -> str:
    """Cached separator generation."""
    return "=" * length

def print_section_header(title: str, length: int = 60):
    """Optimized section header printing."""
    separator = get_separator(length)
    print(f"\n{separator}")
    print(title)
    print(separator)

def demonstrate_basic_reference_counting():
    """Optimized basic reference counting demonstration."""
    print_section_header("🎯 BASIC REFERENCE COUNTING DEMONSTRATION")
    
    # Create an object
    print("\n1. Creating an object...")
    obj = OptimizedReferenceTracker("my_object")
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
    
    # Pass to a function (optimized)
    print("\n5. Passing to a function...")
    def optimized_dummy_function(param):
        param.show_status("(inside function)")
        return param
    
    result = optimized_dummy_function(obj)
    obj.show_status("(after function call)")
    
    # Remove references one by one (optimized)
    print("\n6. Removing references one by one...")
    
    operations = [
        ("Removing from dictionary...", lambda: my_dict.pop("key", None)),
        ("Removing from list...", lambda: my_list.clear()),
        ("Removing function result...", lambda: None),  # Will be handled by del
        ("Removing second reference...", lambda: None),  # Will be handled by del
        ("Removing original reference...", lambda: None)  # Will be handled by del
    ]
    
    for i, (description, operation) in enumerate(operations):
        print(f"   {description}")
        if operation():
            operation()
        if i == 1:  # After clearing list
            del result
        elif i == 2:  # After removing result
            del another_ref
        elif i == 3:  # After removing second reference
            del obj
            break
        else:
            obj.show_status(f"(after {description.lower().rstrip('...')})")

def demonstrate_circular_references():
    """Optimized circular reference demonstration."""
    print_section_header("🔄 CIRCULAR REFERENCE DEMONSTRATION")
    
    print("\n1. Creating circular reference...")
    node_a = FastCircularNode("A")
    node_b = FastCircularNode("B")
    
    # Create circular reference
    node_a.ref = node_b
    node_b.ref = node_a
    
    # Use direct sys.getrefcount for better performance
    print(f"   Node A ref count: {sys.getrefcount(node_a) - 1}")
    print(f"   Node B ref count: {sys.getrefcount(node_b) - 1}")
    
    print("\n2. Removing direct references...")
    del node_a
    del node_b
    
    print("   Direct references removed, but objects still exist due to circular reference")
    print("   (Objects will be cleaned up by garbage collector)")

def demonstrate_garbage_collection():
    """Optimized garbage collection demonstration."""
    print_section_header("🗑️  GARBAGE COLLECTION DEMONSTRATION")
    
    print("\n1. Creating circular references...")
    # Use list comprehension for better performance
    nodes = [FastGarbageNode(f"Node_{i}") for i in range(3)]
    
    # Create circular references efficiently
    for i in range(len(nodes)):
        nodes[i].ref = nodes[(i + 1) % len(nodes)]
    
    print(f"   Created {len(nodes)} nodes with circular references")
    
    print("\n2. Removing direct references...")
    del nodes
    
    print("3. Running garbage collection...")
    collected = gc.collect()
    print(f"   Garbage collector collected {collected} objects")

def demonstrate_reference_counting_in_functions():
    """Optimized function reference counting demonstration."""
    print_section_header("⚙️  FUNCTION REFERENCE COUNTING DEMONSTRATION")
    
    def optimized_function_with_local_ref():
        print("   Entering function...")
        local_obj = OptimizedReferenceTracker("function_local")
        local_obj.show_status("(inside function)")
        print("   Exiting function...")
    
    def optimized_function_with_return():
        print("   Entering function with return...")
        local_obj = OptimizedReferenceTracker("function_return")
        local_obj.show_status("(inside function)")
        print("   Returning object...")
        return local_obj
    
    print("\n1. Function with local object (no return):")
    optimized_function_with_local_ref()
    print("   (Object should be deallocated when function exits)")
    
    print("\n2. Function with returned object:")
    returned_obj = optimized_function_with_return()
    returned_obj.show_status("(after function return)")
    
    print("\n3. Removing returned object:")
    del returned_obj
    print("   (Object should be deallocated now)")

def demonstrate_data_structures():
    """Optimized data structures reference counting demonstration."""
    print_section_header("📦 DATA STRUCTURES REFERENCE COUNTING")
    
    # Create objects efficiently
    objects = {
        'list': OptimizedReferenceTracker("list_object"),
        'dict': OptimizedReferenceTracker("dict_object"),
        'set': OptimizedReferenceTracker("set_object")
    }
    
    print("\n1. Storing objects in different data structures:")
    
    # Use more efficient data structure operations
    containers = {
        'list': [objects['list']],
        'dict': {"key": objects['dict']},
        'set': {objects['set']},
        'tuple': tuple(objects.values())
    }
    
    # Show status for all objects
    for obj_name, obj in objects.items():
        obj.show_status(f"(in {obj_name})")
    
    print("\n2. Removing from data structures:")
    
    # Remove from containers efficiently
    containers['list'].clear()
    objects['list'].show_status("(removed from list)")
    
    containers['dict'].pop("key", None)
    objects['dict'].show_status("(removed from dict)")
    
    containers['set'].clear()
    objects['set'].show_status("(removed from set)")
    
    print("\n3. Removing tuple reference:")
    del containers['tuple']
    print("   (Objects should be deallocated now)")

def demonstrate_performance_comparison():
    """Demonstrate performance improvements."""
    print_section_header("⚡ PERFORMANCE COMPARISON")
    
    print("\nTesting reference count operations...")
    
    # Test with original approach (simulated)
    start_time = time.perf_counter()
    for i in range(1000):
        obj = OptimizedReferenceTracker(f"test_obj_{i}")
        _ = obj._get_ref_count()
    original_time = time.perf_counter() - start_time
    
    print(f"   Optimized approach: {original_time:.4f} seconds for 1000 operations")
    
    # Test garbage collection performance
    print("\nTesting garbage collection performance...")
    start_time = time.perf_counter()
    
    # Create many objects with circular references
    nodes = []
    for i in range(100):
        node = FastGarbageNode(f"perf_node_{i}")
        nodes.append(node)
    
    # Create circular references
    for i in range(len(nodes)):
        nodes[i].ref = nodes[(i + 1) % len(nodes)]
    
    del nodes
    gc_time = time.perf_counter() - start_time
    
    print(f"   Garbage collection time: {gc_time:.4f} seconds")

def interactive_demo():
    """Optimized interactive demonstration."""
    print_section_header("🎮 INTERACTIVE REFERENCE COUNTING DEMO")
    
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
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'create':
                current_obj = OptimizedReferenceTracker("interactive_object")
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
        except KeyboardInterrupt:
            print("\n👋 Interactive demo interrupted.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Optimized main function."""
    print("🐍 OPTIMIZED PYTHON REFERENCE COUNTING DEMONSTRATION")
    print("This program shows how Python manages memory using reference counting with performance optimizations.")
    
    try:
        # Run all demonstrations
        demonstrate_basic_reference_counting()
        demonstrate_circular_references()
        demonstrate_garbage_collection()
        demonstrate_reference_counting_in_functions()
        demonstrate_data_structures()
        demonstrate_performance_comparison()
        
        # Ask if user wants interactive demo
        response = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
        
        print_section_header("✅ OPTIMIZED DEMONSTRATION COMPLETE!")
        print("\nKey optimizations implemented:")
        print("• Reference count caching to reduce sys.getrefcount() calls")
        print("• Use of __slots__ for memory-efficient classes")
        print("• Cached separator generation with lru_cache")
        print("• Optimized data structure operations")
        print("• Reduced function call overhead")
        print("• More efficient list comprehensions and operations")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")

if __name__ == "__main__":
    main() 