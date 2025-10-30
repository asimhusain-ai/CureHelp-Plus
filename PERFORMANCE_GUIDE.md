# Performance Optimization Quick Reference

## For Developers

This guide provides a quick reference for the performance optimizations in CureHelp+.

## Key Optimizations

### 1. Caching with `@lru_cache`

**Files**: `helper.py`, `consultant.py`

Used for pure functions that return the same output for the same input:

```python
from functools import lru_cache

@lru_cache(maxsize=128)  # Cache up to 128 unique calls
def expensive_function(param1, param2):
    # ... computation
    return result
```

**When to use**: Functions with deterministic outputs, frequently called with same parameters.

### 2. Vectorization with NumPy

**Files**: `chatbot.py`

Replace loops with vectorized operations:

```python
# ❌ Slow: Row-by-row iteration
for idx, row in df.iterrows():
    result = compute(row)

# ✅ Fast: Vectorized computation
results = compute(df.values)
```

**When to use**: Operations on arrays/dataframes, mathematical computations.

### 3. I/O Debouncing

**Files**: `profile_manager.py`

Reduce disk writes with time-based throttling:

```python
def save(self, force=False):
    if not force and (time.time() - self._last_save) < threshold:
        return  # Skip save
    # ... save logic
```

**When to use**: Frequent auto-save operations, API calls, file writes.

### 4. Early Exit Optimization

**Files**: `chatbot.py`

Stop searching when good enough result found:

```python
for item in large_list:
    score = compute_score(item)
    if score > 0.9:  # Good enough!
        return item
```

**When to use**: Search operations, pattern matching, validation loops.

### 5. Pre-computation

**Files**: `chatbot.py`

Move expensive operations outside loops:

```python
# ❌ Slow: Compute in every iteration
for item in items:
    words = text.split()  # Computed many times!
    if word in words:
        ...

# ✅ Fast: Compute once
words = text.split()  # Computed once
for item in items:
    if word in words:
        ...
```

**When to use**: Loop-invariant computations.

## Common Patterns

### Pattern: Cache Static Data

```python
@lru_cache(maxsize=1)
def get_static_data():
    return [...]  # Data that never changes
```

### Pattern: Debounce File Saves

```python
self._last_save_time = 0
self._debounce_seconds = 2

def save(self, force=False):
    current = time.time()
    if not force and (current - self._last_save_time) < self._debounce_seconds:
        return
    # ... save
    self._last_save_time = current
```

### Pattern: Vectorize with Pandas/NumPy

```python
# Use .values to get NumPy array
matrix = df[columns].values.astype(float)

# Use vectorized functions
results = numpy_function(matrix)

# Use vectorized indexing
best_idx = np.argmax(results)
```

### Pattern: Session State with Init Flag

```python
if "initialized" not in st.session_state:
    st.session_state.var1 = value1
    st.session_state.var2 = value2
    # ... all initialization
    st.session_state.initialized = True
```

## Performance Checklist

When reviewing code, check for:

- [ ] Loops that could be vectorized with NumPy
- [ ] Pure functions called repeatedly with same args → add `@lru_cache`
- [ ] File I/O in tight loops → debounce or batch
- [ ] Expensive computations inside loops → move outside
- [ ] Full scans that could early exit → add threshold checks
- [ ] Large strings/data rebuilt every time → cache as constant
- [ ] Multiple session state checks → use init flag

## Testing Performance

Run the performance test suite:

```bash
python Tests/test_performance.py
```

Quick performance test:

```python
import time

start = time.time()
result1 = function()
time1 = time.time() - start

start = time.time()
result2 = function()  # Should be cached
time2 = time.time() - start

print(f"First: {time1*1000:.2f}ms, Cached: {time2*1000:.2f}ms")
print(f"Speedup: {time1/time2:.1f}x")
```

## Profiling Code

If you need to identify bottlenecks:

```python
import cProfile
import pstats

# Profile a function
cProfile.run('my_function()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

## Common Mistakes to Avoid

1. **Over-caching**: Don't cache functions with side effects
2. **Cache too large**: Limit cache size to prevent memory issues
3. **Premature optimization**: Profile first, then optimize
4. **Breaking immutability**: Ensure cached function args are immutable
5. **Ignoring edge cases**: Test with small and large datasets

## Best Practices

✅ **Do**:
- Profile before optimizing
- Measure improvements
- Add comments explaining optimizations
- Test for correctness
- Keep API compatible

❌ **Don't**:
- Optimize without measuring
- Make code unreadable for minor gains
- Cache functions with side effects
- Break existing functionality
- Skip testing after optimization

## Resources

- **Detailed Guide**: See `PERFORMANCE_OPTIMIZATIONS.md`
- **Test Suite**: See `Tests/test_performance.py`
- **Summary**: See `OPTIMIZATION_SUMMARY.md`

---

**Last Updated**: 2025-10-30  
**Maintained by**: Development Team
