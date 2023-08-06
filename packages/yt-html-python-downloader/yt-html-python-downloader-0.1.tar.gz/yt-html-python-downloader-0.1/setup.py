from setuptools import setup, find_packages


setup(
    name='yt-html-python-downloader',
    version='0.1',
    license='MIT',
    author="Szymon Flis",
    author_email='flisszymo@wp.pl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/szymoks11/yt-html-python-downloader',
    keywords='yt html python downloader',
    install_requires=[
            'bottle',
            'bottle-websocket',
            'cffi',
            'Eel',
            'ffmpeg-python',
            'future',
            'gevent',
            'gevent-websocket',
            'greenlet',
            'pycparser',
            'pyparsing',
            'pytube',
            'whichcraft',
            'zope.event',
            'zope.interface',
        
      ],

)