from distutils.core import setup

setup(
    name='chase',
    version='1.0',
    description='Simulation of wolfs and sheeps',
    author='RG, JW',
    author_email='216769@edu.p.lodz.pl, 216914@edu.p.lodz.pl',
    url='http://example.com',
    packages=['chase'],  # same as name
    package_dir={'chase': 'src'},
    scripts=[
        'src/wolfs_and_sheeps.py',
        'src/__main__.py',
    ]
)
