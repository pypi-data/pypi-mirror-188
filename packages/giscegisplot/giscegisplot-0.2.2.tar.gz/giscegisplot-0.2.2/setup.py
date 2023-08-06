from setuptools import setup, find_packages
with open('requirements.txt') as f:
    data = f.read()
reqs = data.split()

setup(
    name='giscegisplot',
    version='0.2.2',
    packages=find_packages(),
    url='http://git.gisce.net/gis/giscegisplot',
    license='MIT',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Plot geoms over OSM',
    entry_points='''
        [console_scripts]
        giscegisplot=giscegisplot.plot:get_plot
    ''',
    install_requires=reqs
)
