# AGENTS.md

## AI Code Assistant Guidelines for This Project

This project is a data science codebase. You are an AI code assistant designed to help generate and edit code for this project. Your role is to assist in writing clean, efficient, and well-documented code that adheres to the project's standards and conventions.

Please follow these standards and conventions when generating or editing code:

### 1. Coding Standards

- **PEP8**: All Python code must comply with [PEP8](https://peps.python.org/pep-0008/) style guidelines.
- **Type Hints**: All functions and class methods must include explicit type hints for arguments and return values.
- **Docstrings**: Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings. 

    - Each function/class should have a docstring with an `Args:` section for parameters.
    - When applicable, include `Returns:` and `Raises:` sections. 
    - When iconic notes are needed, use the following format:

        - Use `!!! tip` for useful tips.
        - Use `!!! note` for general notes.
        - Use `!!! warning` for warnings.
        - Use `!!! danger` for critical warnings or dangers.

- **Code Samples**: When including code examples in docstrings avoid using `Example:`. Instead, use triple backticks for code examples within docstrings.

### 2. Docstring Example

```python

variable: str = "This is a variable with a docstring example."
"""This variable is an example of how to include a docstring for a variable."""

def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.

    !!! note
        Additional notes about the function.

    ??? note "Collaspsible Note with Title"
        This is a collapsible note section using a custom title.

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
- Documentation is in `docsrc/mkdocs/` - add new documentation files here and update the mkdocs configuration as needed.

### 4. Documentation - MkDocs Guidance

- Use MkDocs for project documentation. Add new documentation files in `docsrc/mkdocs/`
- If it makes senese to order the documentation, prefix the filenames with numbers (e.g., `01_introduction.md`, `02_usage.md`) to control the order in the navigation, and set the title in the front matter of the markdown file to ensure it appears correctly in the navigation.
- Ensure indentation in markdown files is consistent, multiples of four spaces.
- Use headings (e.g., `#`, `##`, `###`) to structure the documentation clearly.
- For bulleted lists in markdown, use `-` for list items and ensure there is a space after the dash for proper formatting. Also ensure there is a line break before and after the list for better readability.
- Use fenced code blocks with triple backticks for code examples in markdown files, and specify the language for syntax highlighting (e.g., ```python).
- Utilize admonitions in markdown files for important notes, tips, warnings, and dangers using the following syntax:

    - Use `!!! tip` for useful tips.
    - Use `!!! note` for general notes.
    - Use `!!! warning` for warnings about potential issues.
    - Use `!!! danger` for critical warnings or dangers.
    - For collapsible sections in markdown, use the following syntax:

    ``` markdown
    ??? note "Collapsibe Note Title"
        This is the content of the collapsible note.
    ```

- For codeblocks in markdown lists, ensure proper indentation to maintain the list structure. For example:

    ``` markdown
    - Top level list item

        - Nested list item with a code block:

        ``` python
        def nested_example():
        pass
        ```
    ```

### 4. Additional Guidelines

- Prefer clear, descriptive variable and function names.
- Use list comprehensions and generator expressions where it logically makes sense for improved performance.
- When using arcpy to update fields, prefer to use `arcpy.da.UpdateCursor` for better performance, and, if possible, use a generator to feed values into the cursor.
- If performing multiple processing steps using arcpy, use 'memory' workspace for intermediate outputs to enhance performance.
- In all function calls, use keyword arguments following the first positional argument for clarity, especially when there are multiple parameters of the same type.
- When calling arcpy functions, use the more modern `arcpy.toolbox.Tool` syntax, and use all relevant keyword arguments for clarity, even if the function allows positional arguments. This enhances readability and maintainability of the code.
- When working with data, prefer using pandas DataFrames for data manipulation and analysis, and use vectorized operations instead of loops for better performance. If the data is too large for Pandas to handle efficiently, consider using DuckDB for data processing tasks.
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
