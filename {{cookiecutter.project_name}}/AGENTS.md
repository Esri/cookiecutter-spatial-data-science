# AGENTS.md

## AI Code Assistant Guidelines for This Project

This project is a data science codebase. Please follow these standards and conventions when generating or editing code:

### 1. Coding Standards
- **PEP8**: All Python code must comply with [PEP8](https://peps.python.org/pep-0008/) style guidelines.
- **Type Hints**: All functions and class methods must include explicit type hints for arguments and return values.
- **Docstrings**: Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings. Each function/class should have a docstring with an `Args:` section for parameters. When applicable, include `Returns:` and `Raises:` sections. When iconic notes are needed, use the following format:
    - Use `!!! note` for general notes.
    - Use `!!! warning` for warnings.
When including code examples in docstrings avoid using Example: and instead format them as follows:
    - Use triple backticks for code examples within docstrings.

### 2. Docstring Example
```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.

    !!! note
        Additional notes about the function.

    !!! warning
        Warnings about the function usage.

    ``` python
    result = example_function(10, "test")
    print(result)
    ```
    
    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        bool: Description of the return value.
    """
    ...
```

### 3. Project Structure
- Main source code is in `src/{{cookiecutter.project_name}}/`
- Configuration files are in `config/`
- Any credentials or sensitive information should be stored in `config/secrets.ini` (not committed to version control)
- Scripts supporting specific tasks are in `scripts/`
- Data files are in the `data/` directory
- Notebooks are in `notebooks/`
- Tests are in `testing/`

### 4. Additional Guidelines
- Prefer clear, descriptive variable and function names.
- Use list comprehensions and generator expressions where appropriate.
- When using arcpy to update fields, prefer to use `arcpy.da.UpdateCursor` for better performance, and, if possible, use a generator to feed values into the cursor.
- If performing multiple processing steps using arcpy, use 'memory' workspace for intermediate outputs to enhance performance.
- Avoid global variables.
- Write modular, reusable code.
- Add comments for complex logic.
- For data science tasks, prefer pandas, numpy, and scikit-learn when possible.

### 5. AI Assistant Usage
- When generating code, always check for existing functions/classes before creating new ones.
- When editing, preserve existing logic unless explicitly instructed to refactor.
- When adding new files, update relevant documentation and tests.

---

For questions or clarifications, refer to the project README or contact the maintainers.
