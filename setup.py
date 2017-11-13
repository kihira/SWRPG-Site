from setuptools import setup
from os import listdir
from distutils.cmd import Command


class Options:
    """Scour options"""
    indent_type = 'none'
    enable_viewboxing = True
    strip_ids = True
    strip_comments = True
    shorten_ids = True


class OptimiseSVG(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for file in listdir("assets"):
            with open("assets/" + file, "rb") as input, open("server/static/img/" + file, "wb") as output:
                from scour import scour
                scour.start(Options, input, output)


setup(
    name='swrpg-site',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask', 'pymongo'
    ],
    cmdclass={
        'optimise': OptimiseSVG
    }
)
