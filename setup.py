from setuptools import find_namespace_packages, setup


setup(name='xicam.myplugin',
      version='1.0.0',
      author='Eliot',
      install_requires='xicam',
      packages=find_namespace_packages(include=['xicam.*']),
      entry_points={
          'xicam.plugins.GUIPlugin': [
              'SamplePlugin=xicam.myplugin:MyGUIPlugin'
          ],
          'xicam.plugins.OperationPlugin': [
              'invert=xicam.sampleplugin.operations:invert'
              'random_noise=xicam.sampleplugin.operations.noise:random_noise'
          ]
      })
