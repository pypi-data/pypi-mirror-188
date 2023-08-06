from setuptools import setup, find_packages
long_description = open('README.md').read()
setup(
    name='clone-page',
    version='0.0.5',
    author='jaytrairat',
    author_email='jaytrairat@outlook.com',
    description='A script for downloading complete web pages with assets',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['beautifulsoup4', 'requests', 'tqdm'],
    entry_points={
        'console_scripts': [
            'clone-page=clone_page.clone_page:main'
        ]
    }
)
