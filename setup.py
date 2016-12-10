from setuptools import setup, find_packages


setup(
    name="condor",
    packages=find_packages(),
    install_requires=[
        "baseplate",
        "pyramid>=1.7",
        "pyramid_jinja2",
        "sqlalchemy",
    ],
    include_package_data=True,
    tests_require=[
        "nose",
        "coverage",
    ],
)
