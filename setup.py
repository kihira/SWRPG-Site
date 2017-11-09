from setuptools import setup

setup(
    name='swrpg-site',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask', 'pymongo'
    ],
)
