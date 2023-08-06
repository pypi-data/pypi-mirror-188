############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python3
#
# written in python3, (c) 2019-2023 by mworion
# Licence APL2.0
#
###########################################################
from setuptools import setup
from pathlib import Path
import platform

releaseNotes = """
Version 3.0 is a major release! 
Please update with care!
No Python 3.7 support! 
No ARM7 support!
ARM64 only Python 3.8 - 3.9!

- add: GUI: all charts could be zoomed and panned
- add: GUI: all tab menu entries could be customized in order and stored /reset
- add: GUI: all open windows could be collected to visual area
- add: GUI: separate window with big buttons are available 
- add: GUI: reduced GUI configurable for a simpler user interface
- add: video: support for up to 4 external RTSP streams or local cameras
- add: video: adding authentication to video streams
- add: video: adding support for HTTP and HTTPS streams
- add: almanac: now supports UTC / local time
- add: almanac: support set/rise times moon
- add: environment: integrate meteoblue.com seeing conditions
- add: analyse: charts could show horizon and values for each point 
- add: analyse: alt / az charts with iso 2d contour error curves 
- add: audio: sound for connection lost and sat start tracking
- add: model points: multiple variants for edit and move points
- add: model points: set dither on celestial paths
- add: model points: generate from actual used mount model
- add: model points: existing model files could be loaded
- add: model points: golden spiral with exact number of points
- add: polar align: adding hint how to use the knobs measures right
- add: plate solve: new watney astrometry solver for all platforms
- add: hemisphere: selection of terrain file
- add: hemisphere: show actual model error in background
- add: hemisphere: edit horizon model much more efficient
- add: hemisphere: show 2d contour error curve from actual model
- add: hemisphere: move point with mouse around
- add: dome: control azimuth move CW / CCW for INDI
- add: satellites: all time values could be UTC or local time now
- add: MPC / IERS: adding alternative server for download
- add: measure: window has max 5 charts now (from 3)
- add: measure: more values (time delta, focus, cooler power, etc.)
- add: image: photometry functions (aberration, roundness, etc.)
- add: image: tilt estimation like ASTAP does as rectangle and triangle
- add: image: add flip H and flip V
- add: image: show RA/DEC coordinates in image if image was solved
- add: image: center mount pointing g to any point in image by mouse double click
- add: image: center mount pointing to image center
- add: image: support for reading XISF files (simple versions)
- add: imaging: separate page for imaging stats now
- add: imaging: stats: calcs for plate solvers (index files etc.)
- add: imaging: stats: calcs for critical focus zones
- add: drivers: polling timing for drivers could be set
- add: drivers: game controller interface for mount and dome
- add: system: support for python 3.10
- add: help: local install of documentation in PDF format
- add: profiles: automatic translation from v2.2.x to 3.x
- improve: GUI: layout for main window optimized and consistent and wording updates
- improve: GUI: complete rework of charting: performance and functions
- improve: GUI: clean up and optimize IERS download messages
- improve: GUI: get more interaction bullet prove for invalid cross use cases
- improve: GUI: moved on / off mount to their settings: avoid undesired shutoff
- improve: GUI: show twilight and moon illumination in main window
- improve: INDI: correcting setting parameters on startup
- improve: model points: optimized DSO path generation (always fit, less params)
- improve: model run: refactoring
- improve: model run: better information about status and result
- improve: hemisphere: improve solved point presentation (white, red)
- improve: plate solve: compatibility checks 
- improve: system: all log files will be stored in a separate folder /log
- improve: system: enable usage of python 3.10
- improve: system: use latest PyQt5 version 
- improve: system: adjust window sizes to be able to make mosaic layout on desktop
- improve: system: moved to actual jpl kernel de440.bsp for ephemeris calcs
- remove: system: matplotlib package and replace with more performant pyqtgraph
- remove: system: PIL package and replace with more powerful cv2
- remove: system: move from deprecated distutils to packaging
- remove: system: support for python 3.7 as some libraries stopped support
- remove: imageW: stacking in imageW as it was never used
- remove: testing support for OSx Mojave and OSx Catalina (still should work) 
- fix: drivers: device selection tab was not properly positioned in device popup
 """

with open('notes.txt', 'w') as f:
    f.writelines(releaseNotes)

setup(
    name='mountwizzard4',
    version='3.0.0',
    packages=[
        'mw4',
        'mw4.base',
        'mw4.gui',
        'mw4.indibase',
        'mw4.gui.extWindows',
        'mw4.gui.extWindows.hemisphere',
        'mw4.gui.extWindows.image',
        'mw4.gui.extWindows.simulator',
        'mw4.gui.mainWmixin',
        'mw4.gui.mainWindow',
        'mw4.gui.utilities',
        'mw4.gui.widgets',
        'mw4.logic.automation',
        'mw4.logic.camera',
        'mw4.logic.cover',
        'mw4.logic.databaseProcessing',
        'mw4.logic.dome',
        'mw4.logic.environment',
        'mw4.logic.file',
        'mw4.logic.filter',
        'mw4.logic.focuser',
        'mw4.logic.measure',
        'mw4.logic.modeldata',
        'mw4.logic.photometry',
        'mw4.logic.plateSolve',
        'mw4.logic.powerswitch',
        'mw4.logic.profiles',
        'mw4.logic.remote',
        'mw4.logic.telescope',
        'mw4.logic.keypad',
        'mw4.mountcontrol',
        'mw4.resource',
    ],
    python_requires='>=3.8.0, <3.11',
    install_requires=[
        'numpy==1.24.1',
        'opencv-python-headless==4.7.0.68',
        'scipy==1.10.0',
        'astropy==5.2.1',
        'pyerfa==2.0.0.1',
        'astroquery==0.4.6',
        'sep==1.2.1',
        'pyqtgraph==0.13.1',
        'qimage2ndarray==1.10.0',
        'skyfield==1.45',
        'sgp4==2.21',
        'requests==2.28.2',
        'requests_toolbelt==0.10.1',
        'importlib_metadata==6.0.0',
        'python-dateutil==2.8.2',
        'deepdiff==6.2.3',
        'wakeonlan==3.0.0',
        'pybase64==1.2.3',
        'websocket-client==1.5.0',
        'hidapi==0.13.1',
        'range-key-dict==1.1.0',
        'ndicts==0.3.0',
        'packaging==23.0',
        'lz4==4.3.2',
        'xisf==0.9.0',
    ]
    + (['pywin32==305'] if platform.system() == "Windows" else [])
    + (['pywinauto==0.6.8'] if platform.system() == "Windows" else [])
    + (['PyQt5==5.15.8'] if platform.machine() not in ['armv7l'] else [])
    + (['PyQt3D==5.15.6'] if platform.machine() not in ['armv7l',
                                                        'aarch64'] else []),
    keywords=['5.15.8'],
    url='https://github.com/mworion/MountWizzard4',
    license='APL 2.0',
    author='Michael Wuertenberger',
    author_email='michael@wuertenberger.org',
    description='Tool for managing 10micron mounts',
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/x-rst",
    project_urls={
        'Documentation': 'https://mworion.github.io/MountWizzard4',
        'Source Code': 'https://github.com/mworion/mountwizzard4',
        'Bug Tracker': 'https://github.com/mworion/mountwizzard4/issues',
        'Discussions': 'https://github.com/mworion/MountWizzard4/discussions',
        'Channel': 'https://www.youtube.com/user/orion49m/featured',
        'Forum': 'https://www.10micron.eu/forum/',
    },
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Other Environment',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Topic :: Documentation :: Sphinx',
    ]
)
