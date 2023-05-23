from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'A python package to conveniently collect statistics data in ros2'
LONG_DESCRIPTION = 'A package that provides a convenient way to run ROS2 programs multiple times and collect timing and other statistics. It can be used to analyze the performance and behavior of ROS2 systems.'

# Setting up
setup(
    name="ros2-test-runner",
    version=VERSION,
    author="Tharaka Sachintha ",
    author_email="<tharakasachintha27@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ros2', 'humble', 'launch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)