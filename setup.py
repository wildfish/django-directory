from setuptools import setup

f = open('README.md')
readme = f.read()
f.close()

setup(
    name='django-directory',
    version='0.0.1',
    packages=['directory', 'directory.templatetags'],
    url='https://github.com/wildfish/django-directory',
    license='MIT',
    author='dan',
    author_email='dan@wildfish.com',
    description='App for creating a searchable directory of objects',
    long_description=readme,
    package_data={'directory': ['templates/directory/base.html']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    install_requires=[
        'Django>=1.8',
        'django-filter>=0.11.0',
        'six>=1.9.0',
    ],
)
