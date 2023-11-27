#   -*- coding: utf-8 -*-
from sys import path
from pybuilder.core import use_plugin, init, task

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "api"
default_task = "publish"

@init
def set_properties(project):
    project.set_property("coverage_break_build", False) # Set to True when coverage is above threshold
    pass

@task
def run(project):
    path.append("src/main/python")
    from database_api import main  # type: ignore
    main()