from distutils.core import setup

setup(
    name="notify-me-senpy", # name of the package on PyPi
    version="0.5", # version number
    description="Ask senpy to notify you on your phone whenever you need on your python script.", # short textual description
    author="Abiskorp", # authors
    url="https://github.com/magantoine/senpy-package", # link to the repo
    keywords="PRODUCTIVITY",  # can input a list of descriptive keywords TODO COMPLETE
    license="MIT", # can chose licence TODO COMPLETE
    classifiers=[
    'Development Status :: 1 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],

    # link to the release
    download_url="https://github.com/magantoine/senpy-package/archive/refs/tags/0.5.tar.gz"
)