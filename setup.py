from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='cliblog',
    version=0.1,

    description='Add and search posts on a github pages blog',
    long_description=long_description,
    url='https://github.com/rickh94/cliblog',

    author='Rick Henry',
    author_email='fredericmhenry@gmail.com',

    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'ruamel.yaml',
        'click',
        'prompt_toolkit'
    ],
    package=find_packages(),
    entry_points={
        'console_scripts': [
            'cliblog=cliblog.cli:cli',
        ],
    },
)
