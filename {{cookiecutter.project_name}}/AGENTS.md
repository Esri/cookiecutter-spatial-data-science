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
        - Use `!!! note` for general notes.
        - Use `!!! warning` for warnings.
        - use `!!! tip` for useful tips for use.
- **Code Samples**: When including code examples in docstrings avoid using `Example:` and instead format them as follows:
    - Use triple backticks with the language declared for code examples within docstrings.

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

### 3. Markdown Conventions
- **Headings**: Use ATX-style headers (`#`, `##`, `###`, etc.)
- **Lists**: 
    - Use hyphens (`-`) for unordered lists
    - Use numbers for ordered lists
    - Ensure there is a line preceeding lists so they are formatted correctly for MkDocs
- **Emphasis**: Use `*italic*` for emphasis and `**bold**` for strong emphasis
- **Indentation**: Use four spaces for indentation/tabs (not tabs characters)
- **Code**:
    - Use single backticks for inline code: `` `variable_name` ``
    - Use triple backticks with language identifiers for code blocks
    - When including code in docstrings, use triple backticks with the language identifier (e.g., `` ```python ``)
- **Links**: Use descriptive link text: `[link text](URL)`
- **Admonitions**: Use MkDocs-style admonitions in documentation and docstrings:
    - `!!! note` for general information
    - `!!! warning` for important warnings
    - `!!! tip` for helpful tips
    - `!!! danger` for critical warnings
    - `!!! example` for examples
    - **Collapsible Admonitions**: Use `???` instead of `!!!` to make admonitions collapsible by default
    - Use `???+` to make collapsible admonitions expanded by default
- **Tables**: Use pipe-delimited tables with header separators (`|---|---|`)
- **Line Length**: Keep markdown lines under 120 characters when possible for readability
- Follow style guidance and conventions detailed in the [Zensical Documentation](https://zensical.org/docs) under Authoring.

### 4. Project Structure
- Main source code is in `src/{{cookiecutter.project_name}}/`
- Configuration files are in `config/` (use Python files: `config.py`, `secrets.py`)
- Any credentials or sensitive information should be stored in `config/secrets.py` (not committed to version control)
- Scripts supporting specific tasks are in `scripts/`
- Data files are in the `data/` directory
- Notebooks are in `notebooks/`
- Tests are in `testing/`
- Documentation is in `docsrc/mkdocs/` - add new documentation files here and update the mkdocs configuration as needed.

### 5. Additional Guidelines
- Prefer clear, descriptive variable and function names.
- Use list comprehensions and generator expressions where it logically makes sense for improved performance.
- When using arcpy to update fields, prefer to use `arcpy.da.UpdateCursor` for better performance, and, if possible, use a generator to feed values into the cursor.
- When calling arcpy tools, use the convention of `arcpy.toolbox.Toolname` instead of `arcpy.Toolname_toolbox`, and use named parameters for clarity and forward compatibility.
- If performing multiple processing steps using arcpy, use 'memory' workspace for intermediate outputs to enhance performance. Paths become `memory/datasetname` for intermediate datasets.
- Avoid global variables.
- Write modular, reusable code.
- Add comments for complex logic.
- For data science tasks, prefer pandas, numpy, and scikit-learn when possible.
- When assembling data together using joins and relates, if the data is large, large enough to slow down processing using conventional methods, use [DuckDB](https://duckdb.org/docs/stable/).
- Instead of using manual string path manipulation or `os.path` use `pathlib.Path` for platform portability and to create much more readable code.

### 6. AI Assistant Usage
- When generating code, always check for existing functions/classes before creating new ones.
- When editing, preserve existing logic unless explicitly instructed to refactor.
- When adding new files, update relevant documentation and tests.

---

For questions or clarifications, refer to the project README or contact the maintainers.
