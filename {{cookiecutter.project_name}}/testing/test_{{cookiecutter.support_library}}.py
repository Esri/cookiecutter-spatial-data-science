"""
This is a stubbed out test file designed to be used with PyTest, but can 
easily be modified to support any testing framework.
"""

from pathlib import Path
import sys

# get paths to useful resources - notably where the src directory is
self_pth = Path(__file__).absolute
dir_test = self_pth.parent
dir_prj = dir_test.parent
dir_src = dir_prj/'src'

# insert the src directory into the path and import the projct package
sys.path.insert(0, str(dir_src))
import {{cookiecutter.support_library}}

def test_example():
    assert 2 + 2 == 4