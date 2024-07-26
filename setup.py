from setuptools import setup, find_packages

setup(
    name='flask_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'redis',
        'rq'
    ],
    tests_require=[
        'pytest',
        'pytest-flask',
    ],
    entry_points={
        'console_scripts': [
            'runserver=app.main:app.run',
        ],
    },
)
