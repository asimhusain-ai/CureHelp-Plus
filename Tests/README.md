# CureHelp+ Unit Tests

This directory contains comprehensive unit tests for the CureHelp+ application.

## Test Files

### 1. `test_helper.py`
Tests for the recommendation system (`helper.py`):
- Disease recommendation generation for different risk levels
- Risk threshold boundaries (low, medium, high)
- Content quality and relevance of recommendations
- Support for all diseases (Diabetes, Heart Disease, Fever, Anemia)
- Edge cases and boundary values

**Test Count:** 23 tests

### 2. `test_profile_manager.py`
Tests for patient profile management (`profile_manager.py`):
- Profile creation and storage
- JSON serialization and deserialization
- NumPy type conversion for JSON compatibility
- Profile loading and saving
- Data validation and integrity
- Edge cases (empty values, special characters, unicode)

**Test Count:** 21 tests

### 3. `test_consultant.py`
Tests for healthcare provider directory (`consultant.py`):
- Hospital data structure and validation
- Doctor data structure and validation
- Contact information format validation
- URL validity checks
- Data uniqueness and integrity
- Specialization diversity

**Test Count:** 26 tests

### 4. `test_makepdf.py`
Tests for PDF report generation (`makepdf.py`):
- PDF generation for single and multiple diseases
- Risk level visualization
- Input parameter handling
- PDF format validation
- File size and content checks
- Edge cases (empty inputs, extreme values)

**Test Count:** 27 tests

### 5. `test_chatbot.py`
Tests for medical chatbot functionality (`chatbot.py`):
- Input type classification (questions, symptoms, disease names)
- Data cleaning and preprocessing
- Symptom list parsing
- Response structure validation
- Question pattern recognition
- Edge cases (special characters, long inputs)

**Test Count:** 33 tests

## Running Tests

### Run All Tests
```bash
# From the project root directory
python -m unittest discover Tests

# Or from the Tests directory
python -m unittest discover
```

### Run Individual Test Files
```bash
# Test helper module
python -m unittest Tests.test_helper

# Test profile manager
python -m unittest Tests.test_profile_manager

# Test consultant module
python -m unittest Tests.test_consultant

# Test PDF generation
python -m unittest Tests.test_makepdf

# Test chatbot
python -m unittest Tests.test_chatbot
```

### Run Specific Test Class
```bash
python -m unittest Tests.test_helper.TestHelperRecommendations
```

### Run Specific Test Method
```bash
python -m unittest Tests.test_helper.TestHelperRecommendations.test_diabetes_low_risk
```

### Run with Verbose Output
```bash
python -m unittest discover Tests -v
```

## Test Coverage

Total test count: **130 tests**

Coverage by module:
- `helper.py`: 23 tests
- `profile_manager.py`: 21 tests
- `consultant.py`: 26 tests
- `makepdf.py`: 27 tests
- `chatbot.py`: 33 tests

## Requirements

The tests use Python's built-in `unittest` framework and require the following dependencies:
- `pandas` - For data manipulation
- `numpy` - For numerical operations
- `matplotlib` - For PDF generation
- All dependencies from `requirements.txt`

## Test Structure

Each test file follows this structure:
1. **Import statements** - Import the module being tested
2. **Test classes** - Group related tests together
3. **setUp/tearDown methods** - Initialize and clean up test environment
4. **Test methods** - Individual test cases prefixed with `test_`

## Best Practices

- Each test is independent and can run in isolation
- Tests use meaningful assertion messages
- Edge cases and boundary conditions are tested
- Tests clean up after themselves (no side effects)
- Test names clearly describe what is being tested

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m unittest discover Tests -v
```

## Contributing

When adding new features:
1. Write corresponding unit tests
2. Ensure all existing tests pass
3. Follow the existing test structure and naming conventions
4. Aim for high code coverage

## Troubleshooting

### Import Errors
If you get import errors, make sure to run tests from the project root:
```bash
cd /path/to/CureHelp-Plus
python -m unittest discover Tests
```

### Missing Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

### Test Failures
- Check that model files exist in the `models/` directory
- Ensure `chatdata.zip` is present for chatbot tests
- Verify that temporary files are being cleaned up properly

## Test Results

Run tests and check output:
```bash
python -m unittest discover Tests -v 2>&1 | tee test_results.txt
```

## License

These tests are part of the CureHelp+ project and follow the same license.
