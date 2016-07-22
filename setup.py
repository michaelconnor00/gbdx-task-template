from setuptools import setup, find_packages


setup(
    name='gbdx-task-template',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jsonschema==2.4.0',
    ],
    url='https://github.com/michaelconnor00/gbdx-task-template',
    license='MIT',
    description='GBDX Task Template',
    long_description=open('README.rst').read(),
    author='GBDX (Michael Connor)',
    author_email='mike@sparkgeo.com',
    entry_points={},
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    tests_require=['pytest', 'coverage']
)
