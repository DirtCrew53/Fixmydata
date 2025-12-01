from setuptools import setup, find_packages

setup(
    name='fixmydata',
    version='0.1',
    description='A Python library for data cleaning, outlier detection, and data validation.',
    author='Johann Lloyd Megalbio, Albrien Dealino, Shawn Sillote, Rafael John Calingin',
    author_email='megalbio.johann@gmail.com, dealinoalbrien0@gmail.com, shawnsillote03@gmail.com ',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy'
    ],
)
