from distutils.core import setup
setup(
    name = 'tminterface',
    packages = ['tminterface'],
    version = '1.0.2',
    license='GPL3',
    description = 'A client for TMInterface, a TrackMania TAS tool',
    author = 'Adam Bieńkowski',
    author_email = 'donadigos159@gmail.com',
    url = 'https://github.com/donadigo/TMInterfaceClientPython',
    download_url = 'https://github.com/donadigo/TMInterfaceClientPython/archive/refs/tags/0.6.tar.gz',
    keywords = ['TMInterface', 'client', 'TrackMania'],
    install_requires=[
        'bytefield==1.0.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)