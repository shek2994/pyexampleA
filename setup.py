import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyexampleA',
    version='0.0.3',
    author='Som Shekar',
    author_email='shek2994@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shek2994/pyexampleA',
    project_urls = {
        "Bug Tracker": "https://github.com/shek2994/pyexampleA/issues"
    },
    license='MIT',
    packages=['pyexampleA'],
    install_requires=['requests'],
)