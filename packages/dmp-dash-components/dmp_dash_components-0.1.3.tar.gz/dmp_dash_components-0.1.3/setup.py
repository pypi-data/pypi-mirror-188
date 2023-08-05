import json
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

package_name = 'dmp_dash_components'

setup(
    name=package_name,
    version=package["version"],
    author_email=package['email'],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[
        'dash>=2.6.2'
    ],
    classifiers=[
        'Framework :: Dash',
    ],
    url='https://sicsapps.com'
)
