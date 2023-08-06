from setuptools import setup, find_packages

setup(
    name='clone-page',
    version='0.0.2',
    author='jaytrairat',
    author_email='jaytrairat@outlook.com',
    description='A script for downloading complete web pages with assets',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'tqdm'],
    entry_points={
        'console_scripts': [
            'clone-page=clone_page.clone_page:main'
        ]
    }
)
