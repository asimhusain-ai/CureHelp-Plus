# 🧪 CureHelp+ Tests - Quick Reference

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m unittest discover Tests -v

# Run with custom runner
python Tests/run_tests.py
```

## Run Specific Tests
```bash
# Single module
python -m unittest Tests.test_helper

# Single class
python -m unittest Tests.test_helper.TestHelperRecommendations

# Single test
python -m unittest Tests.test_helper.TestHelperRecommendations.test_diabetes_low_risk
```

## Test Files Overview

| File | Tests | Purpose |
|------|-------|---------|
| test_helper.py | 23 | Recommendation system |
| test_profile_manager.py | 21 | Profile management |
| test_consultant.py | 26 | Healthcare directory |
| test_makepdf.py | 27 | PDF generation |
| test_chatbot.py | 33 | Chatbot functionality |
| **TOTAL** | **130** | **Complete coverage** |

## Test Runner Options
```bash
python Tests/run_tests.py --help          # Show help
python Tests/run_tests.py -v             # Verbose mode
python Tests/run_tests.py -q             # Quiet mode
python Tests/run_tests.py --list         # List modules
python Tests/run_tests.py -m test_helper # Run specific module
```

## Expected Output
```
Running all CureHelp+ unit tests...
...............................................
----------------------------------------------------------------------
Ran 130 tests in X.XXXs

OK

✅ ALL TESTS PASSED!
Success Rate: 100.0%
```

## Common Issues

### Import Errors
```bash
# Make sure to run from project root
cd /path/to/CureHelp-Plus
python -m unittest discover Tests
```

### Missing Dependencies
```bash
pip install streamlit pandas numpy matplotlib scikit-learn fpdf
```

## File Structure
```
Tests/
├── README.md           # Full documentation
├── TEST_SUMMARY.md     # Implementation details
├── QUICK_REFERENCE.md  # This file
├── __init__.py         # Package init
├── run_tests.py        # Test runner
├── test_helper.py      # Helper module tests
├── test_profile_manager.py
├── test_consultant.py
├── test_makepdf.py
└── test_chatbot.py
```

## Coverage by Module

### helper.py (23 tests)
✅ Risk levels (low/medium/high)
✅ All diseases (Diabetes, Heart, Fever, Anemia)
✅ Boundary values
✅ Edge cases

### profile_manager.py (21 tests)
✅ Profile CRUD
✅ JSON serialization
✅ NumPy type conversion
✅ Data validation

### consultant.py (26 tests)
✅ Hospital data
✅ Doctor data
✅ Contact validation
✅ Data integrity

### makepdf.py (27 tests)
✅ PDF generation
✅ Multiple diseases
✅ Format validation
✅ Risk visualization

### chatbot.py (33 tests)
✅ Input classification
✅ Data preprocessing
✅ Response structure
✅ Pattern recognition

## CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m unittest discover Tests -v
```

## Adding New Tests

1. Create test file: `Tests/test_newmodule.py`
2. Import module: `from newmodule import function`
3. Create test class: `class TestNewModule(unittest.TestCase)`
4. Add test methods: `def test_feature(self):`
5. Run tests to verify

## Best Practices

✅ Test names describe what's being tested
✅ Each test is independent
✅ Use meaningful assertions
✅ Clean up in tearDown methods
✅ Test both positive and negative cases
✅ Cover edge cases and boundaries

## Need Help?

📖 See Tests/README.md for full documentation
📋 See Tests/TEST_SUMMARY.md for implementation details
💬 Check docstrings in test files
🐛 Report issues on GitHub

---

**Total Tests:** 130 | **Lines of Code:** 2,074 | **Coverage:** All major modules
