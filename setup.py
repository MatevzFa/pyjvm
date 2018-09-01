import errno
import os
from os import path
from sys import path as sys_path

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

this_directory = path.abspath(path.dirname(__file__))
srcdir = path.join(this_directory, "src/")
sys_path.insert(0, srcdir)


def post_install():
    rt_path = os.path.join(os.path.expanduser("~"), '.pyjvmgui')
    try:
        os.makedirs(rt_path)
        print "Created directory '{0}'".format(rt_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass


class DevelopWithRt(develop):
    def run(self):
        develop.run(self)
        post_install()


class InstallWithRt(install):
    def run(self):
        install.run(self)
        post_install()


PYJVMGUI_HOME = os.path.join(os.path.expanduser("~"), '.pyjvmgui')

setup(
    name='pyjvmgui',
    version='1.3.4',
    url='https://github.com/MatevzFa/pyjvm',
    license='GPL-3.0',
    author='matevz',
    author_email='mf6422@student.uni-lj.si',
    description='A GUI for the PyJVM',

    packages=find_packages('src'),
    py_modules=['pyjvmgui'],

    data_files=[
        (PYJVMGUI_HOME, [
            os.path.join('src', 'pyjvm_gui', 'qml', 'App.qml'),
            os.path.join('src', 'pyjvm_gui', 'qml', 'Separator.qml')
        ])
    ],

    package_dir={'': 'src'},

    entry_points={
        'console_scripts': ['pyjvmgui=pyjvmgui:main']
    },

    install_requires=['PySide2'],

    cmdclass={
        'install': InstallWithRt,
        'develop': DevelopWithRt,
    },
)
