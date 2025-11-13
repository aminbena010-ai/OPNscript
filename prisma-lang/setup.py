from setuptools import setup, find_packages

setup(
    name="opn-language",
    version="1.0.0",
    description="OPN Language - A friendly multi-paradigm programming language",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="OPN Language Project",
    url="https://github.com/yourusername/opn-language",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4",
            "black>=23.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "opn=prisma.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords="programming-language transpiler python graphics education ide",
    project_urls={
        "Documentation": "https://github.com/yourusername/opn-language/tree/main/docs",
        "Source": "https://github.com/yourusername/opn-language",
        "Issues": "https://github.com/yourusername/opn-language/issues",
    },
)
