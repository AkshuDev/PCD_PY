from setuptools import setup, find_packages

setup(
    name="pcd_py",
    version="0.0.1",
    description="PCD stands for Python Clipped Dictionaries, that allows you to work with many files with just a few lines. It also allows you to make simple folders with database like functionality and much more.",
    author="Pheonix Community",
    packages=["pcd_py"],
    install_requires=["os", "hashlib", "re", "pickle", "sqlparse", "pyinstaller"]
    )