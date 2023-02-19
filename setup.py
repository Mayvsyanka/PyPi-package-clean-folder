from setuptools import setup, find_namespace_packages

setup(
    name='Clean_Folder_Mary',
    version='0.1.1',
    description='Code for sorting files in directory',
    author="Ovsiannikova Maria",
    url='https://github.com/Mayvsyanka/hometask6',
    author_email='mayvsyanka1@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:start']}
)
