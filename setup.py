# from setuptools import setup

# setup(
#     name='pyexampleA',
#     version='0.1.0',    
#     description='A example Python package',
#     url='https://github.com/shek2994/pyexampleA',
#     author='Som Shekar',
#     author_email='shek2994@gmail.com',
#     license='BSD 2-clause',
#     packages=['pyexampleA'],
#     install_requires=['logging'                     
#                       ],

#     classifiers=[
#         'Development Status :: 1 - Planning',
#         'Intended Audience :: Science/Research',
#         'License :: OSI Approved :: BSD License',  
#         'Operating System :: POSIX :: Linux',        
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.7',
#         'Programming Language :: Python :: 3.9'
#     ],
#     python_requires = ">=3.9"
# )

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