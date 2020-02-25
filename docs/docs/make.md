# Make - Explained

There is a _lot_ of functionality included in the GeoAI-Cookiecutter template. Instead of writing endless documentation detailing how to find and use all these resources, we have created a file, [`make.bat`](blob/master/%7B%7Bcookiecutter.project_name%7D%7D/make.bat), containing shortcuts to accomplish a whole boatload of tasks. 

As with most all the functionality in this template, this came out of our own needs to streamline workflows, and not have to dig all around in the template to get boring and routing tasks accomplished. The commands available in `make.bat` fall into three general categories, data preprocessing, data management, and environment management.

## Data Preprocessing

More than anything else GeoAI-Cookiecutter is designed to streamline the process of geographic feature engineering to create quantitative factors for use in machine learning modeling.

### `> make data`

The initial step of preparing the data for analysis can take a decent amount of time. As you develop the steps for the data preparation pipeline, place them into ./scripts/make_data.py. Then, when you need to prepare data, all you need to do is use this command to build your data for modeling.

## Data Management

Although the code can be synchronized with version control, typically GitHub, datasets can be large, and frequently do not work well with version control. As a result, the data directory is excluded from version control in the `.gitignore` file, and can be saved to Azure Blob Storage.

### `> make get_data`

This is particularly useful when collaborating on a project. After retrieving a project from version control, you can retrieve the data needed for the project using this command. The data will be downloaded from Azure Blob storage using credentials saved in the `.env` file and automatically extracted to the `./data` directory.

### `> make push_data`

This creates a zipped archive of the entire contents of the `./data` directory, and pushes it to Azure Blob storage using credentials saved in the `.env` file.

## Environment Management

Managing the Python Conda environment is dramatically streamlined using the commands contained in `make.bat`. Quite honestly, this is one of the single largest motivating factors for initially creating it.

### `> make env`

This is the most commonly used command. This command creates a Conda environment using the name set up when originally creating the project. Due to some nuances of how Conda is configured with ArcGIS Pro, you cannot simply create a new environment directly from the `environment.yml`. Rather, you have to clone the default ArcGIS Pro Conda environment `arcgispro-py3` and update the new environment using the `environment.yml` file. Additionally, if you like to use the mapping widget in Jupyter Lab, there are two additional steps to configure this as well. Hence, all of this is consolidated into one single step.

### `> make env_activate`

Sometimes the environment name is a little long, and sometimes you cannot recall what it is. Either way, it does not matter. This command will activate the project environment created using the command above, so you can get to work!

### `> make env_remove`

Multiple environments for projects quickly litter your computer. Hence, once finished with an environment for a project, this makes it easier to remove the environment from the machine.