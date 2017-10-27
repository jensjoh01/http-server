from setuptools import setup

setup(
    name="Socket Echo Server",
    install_requires=['ipython'],
    extras_require={'test': ['pytest', 'pytest-watch', 'tox']}

)