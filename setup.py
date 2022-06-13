from setuptools import setup

setup(
	name='alcmixer',
	version='0.1.0',
	author='Daniel Kavoulakos',
	author_email='dan_kavoulakos@hotmail.com',
	description='Create midi drum patterns by randomly combining multiple Ableton Live Clips',
	license='MIT',
	packages=['.alcmixer'],
	install_requires=[
		'note_seq',
		'beautifulsoup4',
		],
	keywords=['Ableton', 'drumkit', 'midi', 'alc'],
	python_requires='>=3.6',

)