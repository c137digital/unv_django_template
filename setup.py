from setuptools import setup, find_packages


setup(
    name='web_app',
    version='0.1',
    description="""Provide description""",
    url='http://github.com/',
    author='',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=[
        'unv.app',
        'unv.deploy',

        'uwsgi',
        'django==3.0b1',
    ],
    extras_require={
        'dev': [
            'psycopg2-binary',
            'pylint',
            'pycodestyle',
            'pytest',
            'pytest-cov',
            'pytest-env',
            'pytest-pythonpath',
            'autopep8',
            'sphinx',
            'setuptools',
            'twine',
        ]
    },
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'manage = app.components.django.bin:manage'
        ]
    }
)
