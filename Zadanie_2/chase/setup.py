from distutils.core import setup

setup(
    name='chase',
    version='1.0',
    description='Simulation of wolf and sheeps',
    author='RG, JW',
    author_email='216769@edu.p.lodz.pl, 216914@edu.p.lodz.pl',
    url='http://example.com',
    packages=['chase'],
    package_dir={'chase': '.'},
    scripts=[
        '.\\Simulate.py',
        '.\\Sheep.py',
        '.\\Wolf.py',
        '.\\__main__.py'
    ]
)
