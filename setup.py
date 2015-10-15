from distutils.core import setup

setup(
    name='emergency',
    version='0.0.0',
    packages=['emergency'],
    url='',
    license='MIT License',
    author='Darwin Monroy',
    author_email='contact@darwinmonroy.com',
    description='Web-based Emergency Management Service',
    install_requires=[
        'chilero',
        'schema-migrations',
        'gunicorn'
    ]
)
