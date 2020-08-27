"""
Flask-Djangoify
-------------

This is the description for that library
"""
from setuptools import setup
from flask_djangoify.djangoify import version


setup(
    name='flask-djangoify',
    version=version,
    url='https://github.com/JohnDing1995/flask-djangoify',
    license='BSD',
    author='Ruiyang Ding',
    author_email='dry950526@gmail.com',
    description='Using flask, in a django way ',
    long_description=__doc__,
    py_modules=['flask_djangoify'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask >= 1.0, <2',
        'blinker >= 1.4, <2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
