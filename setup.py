from distutils.core import setup
import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="notify-me-senpy", # name of the package on PyPi
    version="0.4", # version number
    description="Simple python tracker", # short textual description
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="Notify Me SenPy", # authors
    author_email='notify.me.senpy@gmail.com',
    url="https://github.com/magantoine/senpy-package", # link to the repo
    keywords="PRODUCTIVITY",  # can input a list of descriptive keywords TODO COMPLETE
    license="GPLv3", # can chose licence TODO COMPLETE
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'senpy = senpy.cli:main'
        ]
    },
    install_requires=[
        "colorama==0.4.4",
        "keyring==23.2.1",
        # "PyInquirer==1.0.3",
        "requests==2.26.0",
        "inquirerpy==0.3.0"
      ],
    packages=["senpy"],
    # link to the release
    # download_url="https://github.com/magantoine/senpy-package/archive/refs/tags/0.5.tar.gz"
)
