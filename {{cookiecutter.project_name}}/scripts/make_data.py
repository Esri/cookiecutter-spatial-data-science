import os
import sys

# facilitate using local {{cookiecutter.support_library}} package resources
sys.path.insert(0, os.path.abspath('../src'))
import {{cookiecutter.support_library}}
