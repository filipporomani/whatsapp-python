from os import path
from setuptools import setup

# read the contents of your description file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

test_deps = ["python-dotenv==0.20.0", "pytest==7.1.3"]
extras = {"test": test_deps}

setup(
    name="whatsapp-python",
    version="1.0.2",
    description="Opensource Python wrapper to WhatsApp Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipporomani/whatsapp",
    author="Filippo Romani",
    author_email="mail@filipporomani.it",
    license="MIT",
    packages=["whatsapp"],
    install_requires=["requests", "requests-toolbelt", "typing"],
    tests_require=test_deps,
    extras_require=extras,
    keywords=[
        "whatsapp",
        "whatsapp-libary",
        "WhatsApp Cloud API Wrapper",
        "PyWhatsApp",
        "WhatsApp API in Python",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
