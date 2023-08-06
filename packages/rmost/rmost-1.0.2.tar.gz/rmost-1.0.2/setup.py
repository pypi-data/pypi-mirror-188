import setuptools
with open(r'D:\Users\Ярослав\Desktop\DROPRMOST\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='rmost',
	version='1.0.2',
	author='YarKiy',
	author_email='rosya6721@gmail.com',
	description='Module by R',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['rmost'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10.1',
)