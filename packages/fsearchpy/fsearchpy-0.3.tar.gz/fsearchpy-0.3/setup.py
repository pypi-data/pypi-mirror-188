from setuptools import setup, find_packages

setup(
    name="fsearchpy",
    version="0.03",
    author="Dawood",
    packages=find_packages(),
    install_requires=["pymupdf", "pandas", "numpy", "python-pptx", "python-docx"],
    entry_points={
        "console_scripts": [
            "fsearchpy = fsearchpy.fsearchpy:main",
        ]
    },
)