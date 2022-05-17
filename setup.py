import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()


setuptools.setup(
    name="neo4jVersioning",
    version='1.0.0',
    author="Alexandros Stavroulakis",
    author_email="stavroulakisalexandros@gmail.com",
    description="Package to provide versioning functionalities for neo4j\
         database",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stavroulakis/neo4j_versioning",
    install_requires=['neo4j'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
