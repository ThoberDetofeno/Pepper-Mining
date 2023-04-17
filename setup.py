from setuptools import find_packages, setup

LONG_DESCRIPTION = 'PepperMining is a open source process mining platform written in Python.'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="peppermining",
      version="0.0.1",
      author="Thober Detofeno",
      author_email="thober@gmail.com",
      description="Pepper Mining is a free process mining.",
      long_description=long_description,
      license='MIT',
      long_description_content_type="text/markdown",
      # TODO adicione outros pacotes que precisem ser instalados com o seu pacote. Ex: 'caer'
      # pip install pydot
      install_requires=['numpy', 'pandas', 'pydot', 'deepdiff'],
      url="https://github.com/ThoberDetofeno/peppermining",
      project_urls={
          "Bug Tracker": "https://github.com/ThoberDetofeno/peppermining/issues",
          "repository": "https://github.com/ThoberDetofeno/peppermining/tree/master",
      },
      keywords=['python', 'process mining'],
      classifiers=[
          "Development Status :: 1 - Planning",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_packages(include=["src"]),
      setup_requires=['pytest-runner'],
      tests_require=['pytest==4.4.1'],
      test_suite='tests',
      python_requires=">=3.8",)
