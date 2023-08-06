import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ml_template_engine",                     # This is the name of the package
    version="0.1",                        # The initial release version
    author="Devendra Vyas",                     # Full name of the author
    description="Python based Machine Learning Template engine for creating basic templates for various ML/DL tasks",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ml_template_engine"],             # Name of the python package
    package_dir={'':'ml_template_engine/src'},     # Directory of the source code of the package
    install_requires=[
                      'PyInquirer==1.0.3',
                      'prompt-toolkit==1.0.14',
    ]# Install other dependencies if any
)




# 'click==8.1.3',
#                       'colorama>=0.4.6',
#                       'commonmark>=0.9.1',
#                       'Pygments2.14.0',
#                       'rich==12.6.0',
#                       'shellingham==1.5.0.post1',
#                       'typer==0.7.0',
