# AGENTS.md

## AI Code Assistant Guidelines for This Project

This project was created using the 
[Cookiecutter-Spatial-Data-Science](https://github.com/esri/cookiecutter-spatial-data-science) template, 
which is designed to streamline and promote best practices for projects combining Geography and Data Science. 
It provides a logical, reasonably standardized, and flexible project structure.

You are an AI code assistant designed to help generate and edit code for this project. Your role is to 
assist in writing clean, efficient, and well-documented code that adheres to the project's standards and 
conventions.

### Resources

#### This Project's Template

- **Cookiecutter-Spatial-Data-Science Repository**:
  [https://github.com/esri/cookiecutter-spatial-data-science](https://github.com/esri/cookiecutter-spatial-data-science)
- **Template Issues**:
  [https://github.com/esri/cookiecutter-spatial-data-science/issues](https://github.com/esri/cookiecutter-spatial-data-science/issues)
- **Contributing Guidelines**:
  [https://github.com/esri/contributing](https://github.com/esri/contributing)

#### Cookiecutter Core Documentation

- **Cookiecutter Documentation**:
  [https://cookiecutter.readthedocs.io/](https://cookiecutter.readthedocs.io/)
- **Cookiecutter GitHub**:
  [https://github.com/cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
- **Advanced Features**:
  [https://cookiecutter.readthedocs.io/en/stable/advanced/index.html](https://cookiecutter.readthedocs.io/en/stable/advanced/index.html)

---

## Coding Standards and Conventions

Please follow these standards and conventions when generating or editing code:

### 1. Coding Standards

- **PEP8**: All Python code must comply with [PEP8](https://peps.python.org/pep-0008/) style guidelines.
- **Type Hints**: All functions and class methods must include explicit type hints for arguments and 
  return values.
- **Docstrings**: Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) 
  for docstrings.
    - Each function/class should have a docstring with an `Args:` section for parameters.
    - When applicable, include `Returns:` and `Raises:` sections.
    - When iconic notes are needed, use the following format:
        - Use `!!! tip` for useful tips.
        - Use `!!! note` for general notes.
        - Use `!!! warning` for warnings.
        - Use `!!! danger` for critical warnings or dangers.
- **Code Samples**: When including code examples in docstrings avoid using `Example:`. Instead, use 
  triple backticks for code examples within docstrings.

### 2. Docstring Example

```python
variable: str = "This is a variable with a docstring example."
"""This variable is an example of how to include a docstring for a variable."""

def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.

    !!! note
        Additional notes about the function.

    ??? note "Collapsible Note with Title"
        This is a collapsible note section using a custom title.

    !!! warning
        Warnings about the function usage.

    ```python
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
    - Ensure there is a line preceding lists so they are formatted correctly for MkDocs
- **Emphasis**: Use `*italic*` for emphasis and `**bold**` for strong emphasis
- **Indentation**: Use four spaces for indentation/tabs (not tab characters)
- **Code**:
    - Use single backticks for inline code: `` `variable_name` ``
    - Use triple backticks with language identifiers for code blocks
    - When including code in docstrings, use triple backticks with the language identifier 
      (e.g., `` ```python ``)
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
- Follow style guidance and conventions detailed in the 
  [Zensical Documentation](https://zensical.org/docs) under Authoring.

### 4. Project Structure

This project follows the Cookiecutter-Spatial-Data-Science structure:

- **`src/{{cookiecutter.support_library}}/`** - Main source code for the project package
- **`config/`** - Configuration files (use Python files: `config.py`, `secrets.py`)
    - Any credentials or sensitive information should be stored in `config/secrets.py` 
      (not committed to version control)
- **`scripts/`** - Standalone automation scripts for data processing, toolbox creation, etc.
- **`data/`** - Data files (raw, processed, external, interim)
- **`notebooks/`** - Jupyter notebooks for exploratory analysis
- **`arcgis/`** - ArcGIS Pro project files, Python toolboxes (*.pyt), and layer files
- **`testing/`** - PyTest test files
- **`docsrc/`** - MkDocs documentation source files
- **`reports/`** - Generated reports, figures, and logs
- **`models/`** - Trained models and model metadata (*.emd files)

### 5. Spatial Data Science Best Practices

#### 5.1 General Code Quality

- Prefer clear, descriptive variable and function names
- Avoid global variables
- Write modular, reusable code
- Add comments for complex logic
- Keep functions small and focused on a single responsibility
- Use logging instead of print statements for better control over output
- Handle exceptions gracefully and provide informative error messages
- Avoid hardcoding values; use configuration files or environment variables instead
- Avoid early returns in functions; instead, structure logic to minimize multiple exit points
- Write unit tests for new functionality to ensure code reliability
- Use `pathlib.Path` instead of manual string path manipulation or `os.path` for platform 
  portability and readability

#### 5.2 ArcPy Performance

- Prefer `arcpy.da.UpdateCursor` over older cursor methods for better performance
- Use generator expressions to feed values into cursors when possible
- Always clean up cursors using `with` statements, `del` statements, or as context managers
- When calling arcpy tools, use the convention `arcpy.toolbox.Toolname` instead of 
  `arcpy.Toolname_toolbox`, and use named parameters for clarity and forward compatibility

#### 5.3 Intermediate Data Management

**For small datasets (< tens of thousands of features)**:

- Use the `memory` workspace for intermediate outputs: `memory/datasetname`
- Provides fastest performance for small to moderate datasets
- No cleanup required as data is automatically released

**For large datasets (≥ tens of thousands of features)**:

- Use the `@with_temp_fgdb` decorator from `{{cookiecutter.support_library}}.utils`
- Automatically creates a temporary file geodatabase and cleans it up after function execution
- Prevents memory issues with large intermediate datasets

```python
from {{cookiecutter.support_library}}.utils import with_temp_fgdb
from pathlib import Path

@with_temp_fgdb
def process_large_dataset(input_fc: str, output_fc: str, temp_fgdb: str = None) -> str:
    """
    Process a large dataset using temporary file geodatabase.
    
    Args:
        input_fc: Path to input feature class.
        output_fc: Path to output feature class.
        temp_fgdb: Temporary file geodatabase path (injected by decorator).
    
    Returns:
        str: Path to the output feature class.
    """
    # Use temp_fgdb for intermediate outputs
    intermediate_fc = str(Path(temp_fgdb) / "intermediate")
    arcpy.analysis.Buffer(
        in_features=input_fc,
        out_feature_class=intermediate_fc,
        buffer_distance_or_field="100 METERS"
    )
    arcpy.analysis.Clip(
        in_features=intermediate_fc,
        clip_features=clip_boundary,
        out_feature_class=output_fc
    )
    return output_fc
```

#### 5.4 Data Processing Best Practices

- For large datasets, use DuckDB or similar tools for efficient querying and processing
- Prefer pandas, numpy, and scikit-learn for data manipulation when possible
- When using Pandas, avoid chained indexing to prevent SettingWithCopyWarning; use `.loc` or `.iloc`
- Use vectorized operations in Pandas and NumPy for better performance instead of iterating over 
  rows with loops
- Use list comprehensions and generator expressions where appropriate, but avoid overusing them in 
  complex logic for readability (PEP8 - explicit is better than implicit)
- When assembling data with joins and relates, if the data is large enough to slow down processing 
  using conventional methods, use [DuckDB](https://duckdb.org/docs/stable/)

### 6. Makefile Commands

This project includes a `Makefile` (and `make.cmd` for Windows) with common commands:

- `make env` - Set up the Conda environment with all dependencies
- `make data` - Run the data pipeline (`./scripts/make_data.py`)
- `make pytzip` - Create a distributable zipped archive of the Python toolbox
- `make docserve` - Run live MkDocs documentation server (http://localhost:8000)
- `make docs` - Build the documentation
- `make test` - Run all tests using PyTest
- `make jupyter` - Run Jupyter notebook with options enabling remote connections

!!! note
    These commands are defined in `./make.cmd` (Windows) and `./Makefile` (*nix) if you want to 
    examine, modify or extend this capability.

### 7. AI Assistant Usage Guidelines

- **Before creating**: Always check for existing functions/classes before creating new ones
- **When editing**: Preserve existing logic unless explicitly instructed to refactor
- **When adding files**: Update relevant documentation and tests
- **Version control**: Never commit sensitive information (credentials, API keys) to version control
- **Testing**: Write tests for new functionality in the `testing/` directory
- **Documentation**: Update MkDocs documentation in `docsrc/` when adding significant features

### 8. Documentation Best Practices

- Use **MkDocs** with the Material theme for all documentation
- Place documentation files in `./docsrc/mkdocs/`
- Update `./docsrc/mkdocs.yml` to include new pages in the table of contents
- Use **MkDocStrings** to auto-generate API documentation from Python docstrings
- Move Jupyter Notebooks you want in documentation to `./docsrc/mkdocs/notebooks/`
- Use admonitions (`!!! note`, `!!! warning`, etc.) to highlight important information
- Keep documentation up-to-date with code changes

### 9. Logging Best Practices

- Use the `get_logger` function from `{{cookiecutter.support_library}}.utils` for consistent logging
- Configure loggers at the module level:

    ```python
    from {{cookiecutter.support_library}}.utils import get_logger
    
    logger = get_logger(__name__, level='DEBUG', add_stream_handler=False)
    ```

- In scripts, configure the root logger with file output:

    ```python
    import datetime
    
    logfile_path = dir_logs / f'{script_name}_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log'
    logger = get_logger(level='INFO', add_stream_handler=True, logfile_path=logfile_path)
    ```

- Use appropriate log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

For questions or clarifications, refer to the:

- Project [README.md](README.md)
- [Cookiecutter-Spatial-Data-Science documentation](https://github.com/esri/cookiecutter-spatial-data-science)
- Project maintainers or team leads
