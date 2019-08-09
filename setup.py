from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
]

keywords = [
    'sql', 'sqlite', 'sqlite3', 'database',
    'data-science', 'data-analysis', 'python'
]

setup(
    name='faro',
    version='0.0.1',  # see https://semver.org
    description='An SQL-focused data analysis library for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/yanniskatsaros/faro',
    author='Yannis Katsaros',
    author_email='yanniskatsaros@hotmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas'],
    zip_safe=False,
    classifiers=classifiers,
    keywords=' '.join(keywords)
)
