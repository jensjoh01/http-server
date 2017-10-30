from setuptools import setup

setup(
    name="Socket Echo Server",
    package_dir={'': 'src'},
    my_modules=['server', 'client'],
    install_requires=['ipython', 'requests'],
    extras_require={'test': ['pytest', 'pytest-watch', 'tox']}
)
