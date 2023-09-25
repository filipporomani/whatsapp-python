from os import path
from setuptools import setup
from constants import VERSION

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="whatsapp-python",
    version=VERSION,
    description="Open source Python wrapper for the WhatsApp Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipporomani/whatsapp",
    download_url="https://github.com/filipporomani/whatsapp/releases/latest",
    author="Filippo Romani",
    author_email="mail@filipporomani.it",
    license="MIT",
    packages=["whatsapp"],
    install_requires=["requests", "requests-toolbelt", "typing", "fastapi"],
    keywords=[
        "whatsapp",
        "whatsapp-libary",
        "WhatsApp Cloud API Wrapper",
        "PyWhatsApp",
        "WhatsApp API in Python",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
