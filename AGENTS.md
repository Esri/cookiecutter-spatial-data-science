# AGENTS.md

## AI Code Assistant Guidelines for Cookiecutter-Spatial-Data-Science

### About This Project

**Cookiecutter-Spatial-Data-Science** is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template designed to streamline and promote best practices for projects combining Geography and Data Science. It provides a logical, reasonably standardized, and flexible project structure for spatial data science workflows.

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

## Template Development Guidelines

When working on the Cookiecutter template itself:

### 1. Template Syntax
- **Template variables**: Use `{{cookiecutter.variable_name}}` syntax for template variables
- **Jinja2 logic**: Use `{% if %}` and `{% for %}` for conditional logic in templates
- **Variable naming**: Use lowercase with underscores (snake_case) for variable names in `cookiecutter.json`

### 2. Hooks
- **Post-generation hooks**: Located in `hooks/post_gen_project.py`
- **Pre-generation hooks**: Located in `hooks/pre_gen_project.py` (if needed)
- Hooks should handle setup tasks like:
  - Removing unused files based on user choices
  - Setting up Git repository
  - Creating initial directory structures
  - Validating user input

### 3. Testing the Template
- Test template generation with different configurations
- Verify all conditional logic works correctly
- Ensure hooks execute without errors
- Test on multiple platforms (Windows, macOS, Linux)
- Use `cookiecutter --replay` to test with previous configurations

### 4. Documentation
- Keep the main `README.md` up to date with:
  - Installation instructions
  - Usage examples
  - Template variable descriptions
  - Project structure overview
- Update `docsrc/` documentation for significant template changes
- Document any new template variables in `cookiecutter.json`

### 5. Version Control
- Never include actual credentials or API keys in the template
- Use placeholder values for sensitive configuration
- Include appropriate `.gitignore` files in the template

---

!!! note
    Projects generated from this template have their own `AGENTS.md` file with project-specific coding guidelines. This file focuses solely on template development.

For questions, clarifications, or to report issues:
1. Check the [project documentation](https://github.com/esri/cookiecutter-spatial-data-science)
2. Search [existing issues](https://github.com/esri/cookiecutter-spatial-data-science/issues)
3. Submit a new issue if needed
4. Contact the maintainers at Esri
