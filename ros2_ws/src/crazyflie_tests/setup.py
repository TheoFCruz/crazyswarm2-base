import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'crazyflie_tests'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='theofc',
    maintainer_email='theofonsecacruz@gmail.com',
    description='Tests for trajectory tracking and collision avoidance in crazyswarm2 and crazyflie',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'collision_avoidance = crazyflie_tests.collision_avoidance:main',
            'hover_to_fullstate = crazyflie_tests.hover_to_fullstate:main'
        ],
    },
)
