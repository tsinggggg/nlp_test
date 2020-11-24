from setuptools import setup, find_packages

from __init__ import __version__


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nlptest',
    version=__version__,
    packages=find_packages(exclude=['tests*',
                                    'wandb*'
                                    ]),
    install_requires=requirements,
    description="NLP tests",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    include_package_data=True
)