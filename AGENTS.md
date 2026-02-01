# AGENTS.md

## AI Code Assistant Guidelines for Cookiecutter-Spatial-Data-Science

### About This Project

**Cookiecutter-Spatial-Data-Science** is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template designed to streamline and promote best practices for projects combining Geography and Data Science. It provides a logical, reasonably standardized, and flexible project structure that encourages:

- **Project bootstrapping** - Quick setup of new spatial data science projects
- **Innovation** - Focus on solving problems rather than project setup
- **Repeatability** - Consistent project structure across teams and organizations
- **Documentation** - Built-in documentation framework using MkDocs
- **Best practices** - Industry-standard conventions for Python and spatial analysis

This template integrates seamlessly with ArcGIS Pro and leverages the power of Conda environments, making it ideal for geospatial data science workflows.

### Resources

#### This Project
- **Project Repository**: [https://github.com/esri/cookiecutter-spatial-data-science](https://github.com/esri/cookiecutter-spatial-data-science)
- **Issues & Discussions**: [https://github.com/esri/cookiecutter-spatial-data-science/issues](https://github.com/esri/cookiecutter-spatial-data-science/issues) - Search for solutions or report bugs
- **Contributing Guidelines**: [https://github.com/esri/contributing](https://github.com/esri/contributing)

#### Cookiecutter Core Documentation
- **Cookiecutter Documentation**: [https://cookiecutter.readthedocs.io/](https://cookiecutter.readthedocs.io/) - Main documentation
- **Cookiecutter GitHub**: [https://github.com/cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter) - Core project repository
- **Installation Guide**: [https://cookiecutter.readthedocs.io/en/stable/installation.html](https://cookiecutter.readthedocs.io/en/stable/installation.html)
- **Usage Guide**: [https://cookiecutter.readthedocs.io/en/stable/usage.html](https://cookiecutter.readthedocs.io/en/stable/usage.html)
- **Template Development**: [https://cookiecutter.readthedocs.io/en/stable/tutorials.html](https://cookiecutter.readthedocs.io/en/stable/tutorials.html)
- **Advanced Features**: [https://cookiecutter.readthedocs.io/en/stable/advanced/index.html](https://cookiecutter.readthedocs.io/en/stable/advanced/index.html) - Hooks, templating, replay, etc.

---

## Coding Standards and Conventions

When generating or editing code for this Cookiecutter template or projects created from it, follow these guidelines:

### 1. Coding Standards
- **PEP8**: All Python code must comply with [PEP8](https://peps.python.org/pep-0008/) style guidelines.
- **Type Hints**: All functions and class methods must include explicit type hints for arguments and return values.
- **Docstrings**: Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings. Each function/class should have a docstring with an `Args:` section for parameters. When applicable, include `Returns:` and `Raises:` sections. When iconic notes are needed, use the following format:
    - Use `!!! note` for general notes.
    - Use `!!! warning` for warnings.
- **Code Examples**: When including code examples in docstrings, avoid using "Example:" and instead format them as follows:
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

The Cookiecutter template generates projects with the following structure:

- **`src/{{cookiecutter.project_name}}/`** - Main source code for the project package
- **`config/`** - Configuration files (use `secrets.ini` for credentials, never commit to version control)
- **`scripts/`** - Utility scripts for data processing, toolbox creation, etc.
- **`data/`** - Data files (raw, processed, external)
- **`notebooks/`** - Jupyter notebooks for exploratory analysis
- **`arcgis/`** - ArcGIS Pro project files, Python toolboxes (*.pyt), and layer files
- **`testing/`** - PyTest test files
- **`docsrc/`** - MkDocs documentation source files
- **`reports/`** - Generated reports, figures, and logs
- **`models/`** - Trained models and model metadata (*.emd files)

### 4. Spatial Data Science Best Practices

- **ArcPy Performance**:
  - Prefer `arcpy.da.UpdateCursor` over older cursor methods for better performance
  - Use generator expressions to feed values into cursors when possible
  - Use 'memory' workspace for intermediate outputs to enhance performance
  - Always clean up cursors with `del` or use them as context managers

- **Data Processing**:
  - Prefer pandas, numpy, and scikit-learn for data manipulation when possible
  - Use list comprehensions and generator expressions where appropriate
  - For large datasets, consider chunking and streaming approaches

- **Code Quality**:
  - Prefer clear, descriptive variable and function names
  - Avoid global variables
  - Write modular, reusable code
  - Add comments for complex logic
  - Keep functions small and focused on a single responsibility

### 5. Makefile Commands

This template includes a `Makefile` with common commands:

- `make env` - Set up the Conda environment with all dependencies
- `make data` - Run the data pipeline (`./scripts/make_data.py`)
- `make pytzip` - Create a distributable zipped archive of the Python toolbox
- `make docserve` - Run live MkDocs documentation server (http://localhost:8000)
- `make docs` - Build the documentation
- `make test` - Run all tests using PyTest

### 6. AI Assistant Usage Guidelines

- **Before creating**: Always check for existing functions/classes before creating new ones
- **When editing**: Preserve existing logic unless explicitly instructed to refactor
- **When adding files**: Update relevant documentation and tests
- **Version control**: Never commit sensitive information (credentials, API keys) to version control
- **Testing**: Write tests for new functionality in the `testing/` directory
- **Documentation**: Update MkDocs documentation in `docsrc/` when adding significant features

### 7. Template Development

When working on the Cookiecutter template itself:

- **Template variables**: Use `{{cookiecutter.variable_name}}` syntax for template variables
- **Jinja2 logic**: Use `{% if %}` and `{% for %}` for conditional logic in templates
- **Hooks**: Post-generation hooks are in `hooks/post_gen_project.py`
- **Testing**: Test the template generation with different configurations
- **Documentation**: Keep the main README.md and documentation in `docsrc/` up to date

---

For questions, clarifications, or to report issues, please:
1. Check the [project documentation](https://github.com/esri/cookiecutter-spatial-data-science)
2. Search [existing issues](https://github.com/esri/cookiecutter-spatial-data-science/issues)
3. Submit a new issue if needed
4. Contact the maintainers at Esri
