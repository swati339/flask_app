from setuptools import setup, find_packages

setup(
    name='my_flask_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    entry_points={
        'console_scripts': [
            'run-app=app.__init__:app.run',
        ],
    },
)
