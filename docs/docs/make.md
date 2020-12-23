# Make - Explained

There is a _lot_ of functionality included in the GeoAI-Cookiecutter template. Instead of writing endless documentation detailing how to find and use all these resources, we have created a file, [`make.bat`](https://github.com/Esri/geoai-cookiecutter/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/make.bat), containing shortcuts to accomplish a whole boatload of tasks. 

As with most all the functionality in this template, this came out of our own needs to streamline workflows, and not have to dig all around in the template to get boring and routing tasks accomplished. The commands available in `make.bat` fall into three general categories, data preprocessing, data management, and environment management.

## Data Preprocessing

More than anything else GeoAI-Cookiecutter is designed to streamline the process of geographic feature engineering to create quantitative factors for use in machine learning modeling.

### `> make data`

The initial step of preparing the data for analysis can take a decent amount of time. As you develop the steps for the data preparation pipeline, place them into ./scripts/make_data.py. Then, when you need to prepare data, all you need to do is use this command to build your data for modeling.

## Environment Management

Managing the Python Conda environment is dramatically streamlined using the commands contained in `make.bat`. Quite honestly, this is one of the single largest motivating factors for initially creating it. These are the two most common commands, but there are more in there if you want to look.

### `> make env`

This is the most commonly used command. This command creates a Conda environment using the name set up when originally creating the project, and also installs the local module using pip in experimental mode. This means your custom code built to accompnay the module will be available in this new conda environment.

### `> make env_remove`

Multiple environments for projects quickly litter your computer. Hence, once finished with an environment for a project, this makes it easier to remove the environment from the machine.

### `> make ec2`

This is only included in the Linux version in `Makefile`. This is used to configure an AWS EC2 instance to be able to run your project _if your project does not require `arcpy`_.