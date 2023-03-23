from setuptools import setup

setup(
    name='gpt_assist',
    version='0.1.0',
    py_modules=['gpt_assist'],
    install_requires=['openai'],
    entry_points={
        'console_scripts': [
            'gpt_take_the_wheel=gpt_assist:take_the_wheel',
            'gpt_assist=gpt_assist:main',
        ],
    },
)