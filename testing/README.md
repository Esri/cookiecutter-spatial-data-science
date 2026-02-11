# Testing Cookiecutter-Spatial-Data-Science Template

This directory contains tests for validating the Cookiecutter template generation process.

## Overview

This testing suite uses **pytest-cookies**, a pytest plugin specifically designed for testing Cookiecutter templates. The tests verify that the template generates correctly and produces a valid project structure with all required files and configurations.

## pytest-cookies

### What is pytest-cookies?

pytest-cookies provides a `cookies` pytest fixture that simplifies testing Cookiecutter templates by:
- Automatically detecting your `cookiecutter.json` configuration
- Creating temporary directories for test project generation
- Providing a `bake()` method to generate projects with custom context
- Cleaning up temporary directories after tests complete

### Documentation Resources

- **GitHub Repository**: [https://github.com/hackebrot/pytest-cookies](https://github.com/hackebrot/pytest-cookies)
- **PyPI Package**: [https://pypi.org/project/pytest-cookies/](https://pypi.org/project/pytest-cookies/)
- **Documentation**: [https://pytest-cookies.readthedocs.io/](https://pytest-cookies.readthedocs.io/)

### Installation

```bash
pip install pytest-cookies
```

## Running Tests

From the project root directory:

```bash
# Run all tests
pytest

# Run tests in this directory only
pytest testing/

# Run a specific test file
pytest testing/test_sik_project.py

# Run with verbose output
pytest testing/ -v

# Run with debug logging output (see print statements)
pytest testing/ -s

# Run with coverage report
pytest testing/ --cov
```

## How the `cookies` Fixture Works

The `cookies` fixture is automatically injected by pytest-cookies and provides:

1. **`cookies.bake(extra_context={})`** - Generates a project from the template
   - `extra_context`: Dictionary of values to override defaults in `cookiecutter.json`
   
2. **`result.exit_code`** - Exit code of the generation process (0 = success)

3. **`result.exception`** - Any exception raised during project generation

4. **`result.project`** - `pathlib.Path` object pointing to the generated project directory

5. **`result.context`** - The complete context dictionary used for generation

## Test Structure

### test_sik_project.py

This test generates a sample project called "sik-project" and validates:

1. **Successful Generation**: Verifies the template generates without errors
2. **Required Files**: Checks that all expected files and directories are created
3. **Environment Setup**: Tests that `make env` successfully creates a Conda environment
4. **Documentation Build**: Validates that `make docs` builds MkDocs documentation

The test uses a predefined context dictionary to simulate user input:

```python
CONTEXT = {
    "project_name": "sik-project",
    "project_title": "Sik Project",
    "author_name": "One Rad Dude",
    "description": "One sik project by one rad dude.",
    "open_source_license": "Apache 2.0",
    "create_github_repo": "no",
}
```

## Writing New Tests

When adding new tests for the template:

1. **Use descriptive test names**: `test_feature_name` that clearly indicate what is being tested

2. **Follow the pattern**:
   ```python
   def test_my_feature(cookies):
       # Arrange: Define context
       context = {"project_name": "test-project"}
       
       # Act: Generate project
       result = cookies.bake(extra_context=context)
       
       # Assert: Validate results
       assert result.exit_code == 0
       assert result.exception is None
       assert (result.project / "expected_file.txt").exists()
   ```

3. **Test different configurations**: Use different context values to test conditional logic in templates

4. **Validate hook execution**: Ensure post-generation hooks (`hooks/post_gen_project.py`) run correctly

5. **Check file content**: Don't just verify files exist—validate their content when necessary

## Best Practices

- **Keep tests isolated**: Each test should be independent
- **Clean context**: Use minimal context overrides for focused testing
- **Test edge cases**: Verify template behavior with unusual inputs
- **Document assumptions**: Add comments explaining what each test validates
- **Fast tests**: Keep tests quick; avoid unnecessary subprocess calls when possible
- **Use parametrize**: Test multiple scenarios with `@pytest.mark.parametrize`

## Continuous Integration

These tests run automatically on:
- Pull requests
- Commits to the master branch
- Scheduled builds

Ensure all tests pass before submitting a pull request.

## Troubleshooting

### Test Failures

If a test fails:
1. Check the test output for specific assertion errors
2. Examine the generated project in the temporary directory (if preserved)
3. Verify your `cookiecutter.json` is valid
4. Ensure hooks execute without errors
5. Run with `-s` flag to see detailed logging output

### Common Issues

- **Missing dependencies**: Ensure `pytest-cookies` is installed
- **Hook failures**: Check `hooks/post_gen_project.py` for errors
- **Template syntax errors**: Validate Jinja2 syntax in template files
- **Path issues**: Use `pathlib.Path` for cross-platform compatibility

## Contributing

When modifying the template:
1. Update tests to cover new features
2. Run tests locally before committing
3. Ensure CI passes before merging
4. Update this README if test patterns change

For more information about contributing, see [CONTRIBUTING.md](../CONTRIBUTING.md).