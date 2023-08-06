from setuptools import setup

setup(
   name='pytypechecker',
   version='1.0.2',
   author='Sondre Kværne Hansen',
   author_email='sondrekhansen+pypi@gmail.com',
   packages=['typechecker'],
   url='https://github.com/sondrekh/python_typechecker',
   license='LICENCE.txt',
   description='Includes decorator "@typecheck" to provide type check on run-time.',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown"
)