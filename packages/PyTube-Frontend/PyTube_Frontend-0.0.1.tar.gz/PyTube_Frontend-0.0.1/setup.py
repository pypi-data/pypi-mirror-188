from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Frontend for PyTube'
LONG_DESCRIPTION = 'Making PyTube slightly simpler to use and with observer-based status messageing'

# Setting up
setup(
    name="PyTube_Frontend",
    version=VERSION,
    author="ewbrowntech (Ethan Brown)",
    author_email="<ewbrowntech@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'pytube', 'API'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)