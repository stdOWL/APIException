from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="apiexception",
    version="0.1.16",
    description="Consistent JSON response formatting and error handling for FastAPI applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ahmet Kutay URAL",
    author_email="ahmetkutayural@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "fastapi>=0.115.4",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "APIException-info=api_exception.__main__:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Typing :: Typed",
    ],
    project_urls={
        "Documentation": "https://akutayural.github.io/APIException/",
        "Source": "https://github.com/akutayural/APIException",
        "PyPI": "https://pypi.org/project/APIException/",
    },
)
