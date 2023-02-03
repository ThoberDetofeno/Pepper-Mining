from setuptools import setup

LONG_DESCRIPTION = 'PepperMining is a open source process mining platform written in Python.'

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
        name="peppermining", 
        version = "0.0.1",
        author="Thober Detofeno",
        author_email="thober@gmail.com",
        description="Pepper Mining is a free process mining.",
        long_description=long_description,
        long_description_content_type = "text/markdown",
        install_requires=[], # adicione outros pacotes que precisem ser instalados com o seu pacote. Ex: 'caer'
        url = "package URL",
        project_urls = {
            "Bug Tracker": "package issues URL",
        },        
        keywords=['python', 'process mining'],
        classifiers= [
            "Development Status :: 1 - Planning",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        package_dir = {"": "src"},
        packages = setuptools.find_packages(where="src"),
        python_requires = ">=3.8"
)
