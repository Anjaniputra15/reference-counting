#!/usr/bin/env python3
"""
Performance Benchmark for Reference Counting Demonstrations
Compares the original and optimized versions.
"""

import sys
import time
import gc
from typing import Dict, List

# Import both versions
from reference_counting_demo import ReferenceTracker
from reference_counting_demo_optimized import OptimizedReferenceTracker, FastCircularNode, FastGarbageNode

def benchmark_reference_count_operations():
    """Benchmark reference count operations."""
    print("🔍 BENCHMARKING REFERENCE COUNT OPERATIONS")
    print("=" * 60)
    
    # Test original approach
    print("\nTesting original ReferenceTracker...")
    start_time = time.perf_counter()
    original_objects = []
    
    for i in range(1000):
        obj = ReferenceTracker(f"original_obj_{i}")
        original_objects.append(obj)
        # Simulate multiple reference count checks
        for _ in range(5):
            _ = obj.get_ref_count()
    
    original_time = time.perf_counter() - start_time
    print(f"   Original approach: {original_time:.4f} seconds")
    
    # Clean up
    del original_objects
    gc.collect()
    
    # Test optimized approach
    print("\nTesting optimized OptimizedReferenceTracker...")
    start_time = time.perf_counter()
    optimized_objects = []
    
    for i in range(1000):
        obj = OptimizedReferenceTracker(f"optimized_obj_{i}")
        optimized_objects.append(obj)
        # Simulate multiple reference count checks
        for _ in range(5):
            _ = obj._get_ref_count()
    
    optimized_time = time.perf_counter() - start_time
    print(f"   Optimized approach: {optimized_time:.4f} seconds")
    
    # Calculate improvement
    improvement = ((original_time - optimized_time) / original_time) * 100
    print(f"\n   Performance improvement: {improvement:.1f}%")
    
    # Clean up
    del optimized_objects
    gc.collect()

def benchmark_object_creation():
    """Benchmark object creation speed."""
    print("\n🔍 BENCHMARKING OBJECT CREATION")
    print("=" * 60)
    
    # Test original circular nodes
    print("\nTesting original circular nodes...")
    start_time = time.perf_counter()
    original_nodes = []
    
    for i in range(1000):
        node = type('CircularNode', (), {
            '__init__': lambda self, name: setattr(self, 'name', name),
            '__del__': lambda self: None
        })(f"original_node_{i}")
        original_nodes.append(node)
    
    original_time = time.perf_counter() - start_time
    print(f"   Original nodes: {original_time:.4f} seconds")
    
    # Clean up
    del original_nodes
    gc.collect()
    
    # Test optimized circular nodes with __slots__
    print("\nTesting optimized FastCircularNode...")
    start_time = time.perf_counter()
    optimized_nodes = []
    
    for i in range(1000):
        node = FastCircularNode(f"optimized_node_{i}")
        optimized_nodes.append(node)
    
    optimized_time = time.perf_counter() - start_time
    print(f"   Optimized nodes: {optimized_time:.4f} seconds")
    
    # Calculate improvement
    improvement = ((original_time - optimized_time) / original_time) * 100
    print(f"\n   Performance improvement: {improvement:.1f}%")
    
    # Clean up
    del optimized_nodes
    gc.collect()

def benchmark_memory_usage():
    """Benchmark memory usage."""
    print("\n🔍 BENCHMARKING MEMORY USAGE")
    print("=" * 60)
    
    import psutil
    import os
    
    def get_memory_usage():
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    # Test original approach
    print("\nTesting original approach memory usage...")
    initial_memory = get_memory_usage()
    
    original_objects = []
    for i in range(10000):
        obj = ReferenceTracker(f"mem_test_{i}")
        original_objects.append(obj)
    
    original_memory = get_memory_usage()
    original_increase = original_memory - initial_memory
    
    print(f"   Original memory increase: {original_increase:.2f} MB")
    
    # Clean up
    del original_objects
    gc.collect()
    
    # Test optimized approach
    print("\nTesting optimized approach memory usage...")
    initial_memory = get_memory_usage()
    
    optimized_objects = []
    for i in range(10000):
        obj = OptimizedReferenceTracker(f"mem_test_{i}")
        optimized_objects.append(obj)
    
    optimized_memory = get_memory_usage()
    optimized_increase = optimized_memory - initial_memory
    
    print(f"   Optimized memory increase: {optimized_increase:.2f} MB")
    
    # Calculate improvement
    if original_increase > 0:
        memory_improvement = ((original_increase - optimized_increase) / original_increase) * 100
        print(f"\n   Memory efficiency improvement: {memory_improvement:.1f}%")
    
    # Clean up
    del optimized_objects
    gc.collect()

def benchmark_garbage_collection():
    """Benchmark garbage collection performance."""
    print("\n🔍 BENCHMARKING GARBAGE COLLECTION")
    print("=" * 60)
    
    # Test original approach
    print("\nTesting original garbage collection...")
    start_time = time.perf_counter()
    
    # Create circular references
    original_nodes = []
    for i in range(100):
        node = type('GarbageNode', (), {
            '__init__': lambda self, name: setattr(self, 'name', name),
            '__del__': lambda self: None
        })(f"gc_test_{i}")
        original_nodes.append(node)
    
    # Create circular references
    for i in range(len(original_nodes)):
        original_nodes[i].ref = original_nodes[(i + 1) % len(original_nodes)]
    
    del original_nodes
    gc.collect()
    
    original_time = time.perf_counter() - start_time
    print(f"   Original GC time: {original_time:.4f} seconds")
    
    # Test optimized approach
    print("\nTesting optimized garbage collection...")
    start_time = time.perf_counter()
    
    # Create circular references with optimized nodes
    optimized_nodes = []
    for i in range(100):
        node = FastGarbageNode(f"gc_test_{i}")
        optimized_nodes.append(node)
    
    # Create circular references
    for i in range(len(optimized_nodes)):
        optimized_nodes[i].ref = optimized_nodes[(i + 1) % len(optimized_nodes)]
    
    del optimized_nodes
    gc.collect()
    
    optimized_time = time.perf_counter() - start_time
    print(f"   Optimized GC time: {optimized_time:.4f} seconds")
    
    # Calculate improvement
    improvement = ((original_time - optimized_time) / original_time) * 100
    print(f"\n   GC performance improvement: {improvement:.1f}%")

def benchmark_data_structure_operations():
    """Benchmark data structure operations."""
    print("\n🔍 BENCHMARKING DATA STRUCTURE OPERATIONS")
    print("=" * 60)
    
    # Test original approach
    print("\nTesting original data structure operations...")
    start_time = time.perf_counter()
    
    original_objects = [ReferenceTracker(f"ds_test_{i}") for i in range(1000)]
    
    # Store in various data structures
    original_list = original_objects[:100]
    original_dict = {f"key_{i}": obj for i, obj in enumerate(original_objects[100:200])}
    original_set = set(original_objects[200:300])
    original_tuple = tuple(original_objects[300:400])
    
    # Perform operations
    for _ in range(100):
        original_list.append(original_objects[0])
        original_dict[f"new_key_{_}"] = original_objects[0]
        original_set.add(original_objects[0])
    
    original_time = time.perf_counter() - start_time
    print(f"   Original DS operations: {original_time:.4f} seconds")
    
    # Clean up
    del original_objects, original_list, original_dict, original_set, original_tuple
    gc.collect()
    
    # Test optimized approach
    print("\nTesting optimized data structure operations...")
    start_time = time.perf_counter()
    
    optimized_objects = [OptimizedReferenceTracker(f"ds_test_{i}") for i in range(1000)]
    
    # Store in various data structures
    optimized_list = optimized_objects[:100]
    optimized_dict = {f"key_{i}": obj for i, obj in enumerate(optimized_objects[100:200])}
    optimized_set = set(optimized_objects[200:300])
    optimized_tuple = tuple(optimized_objects[300:400])
    
    # Perform operations
    for _ in range(100):
        optimized_list.append(optimized_objects[0])
        optimized_dict[f"new_key_{_}"] = optimized_objects[0]
        optimized_set.add(optimized_objects[0])
    
    optimized_time = time.perf_counter() - start_time
    print(f"   Optimized DS operations: {optimized_time:.4f} seconds")
    
    # Calculate improvement
    improvement = ((original_time - optimized_time) / original_time) * 100
    print(f"\n   DS operations improvement: {improvement:.1f}%")
    
    # Clean up
    del optimized_objects, optimized_list, optimized_dict, optimized_set, optimized_tuple
    gc.collect()

def main():
    """Run all benchmarks."""
    print("🚀 PERFORMANCE BENCHMARK FOR REFERENCE COUNTING DEMONSTRATIONS")
    print("Comparing original vs optimized implementations")
    
    try:
        # Run all benchmarks
        benchmark_reference_count_operations()
        benchmark_object_creation()
        
        # Try memory benchmark (requires psutil)
        try:
            benchmark_memory_usage()
        except ImportError:
            print("\n⚠️  Memory benchmark skipped (psutil not installed)")
            print("   Install with: pip install psutil")
        
        benchmark_garbage_collection()
        benchmark_data_structure_operations()
        
        print("\n" + "=" * 60)
        print("✅ BENCHMARK COMPLETE!")
        print("=" * 60)
        print("\nSummary of optimizations:")
        print("• Reference count caching reduces repeated sys.getrefcount() calls")
        print("• __slots__ reduces memory overhead for simple classes")
        print("• Optimized data structure operations")
        print("• More efficient object creation and cleanup")
        
    except KeyboardInterrupt:
        print("\n\n👋 Benchmark interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during benchmark: {e}")

if __name__ == "__main__":
    main() 