from setuptools import setup

setup(
    name='scany',
    version='1.0.0',
    py_modules=['scany'],
    install_requires=[
        "selenium",
        "selenium-wire",
        "webdriver-manager",
        "openpyxl",
        "typing",
        "pydantic",
        "pytest",
        "bs4",
        "lxml",
        "pandas",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'scany = scany.cli:cli',
        ],
    },
)