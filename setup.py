from setuptools import setup

setup(
    name="visJS2jupyter",
    packages=["visJS2jupyter"],
    version="0.1.10.s231644+git",
    description="visJS2jupyter is a tool to bring the interactivity of networks "
                "created with vis.js into Jupyter notebook cells",
    long_description="0.1.10.s231644: the graphs are now supported in browsers.",
    url="https://github.com/s231644/visJS2jupyter",
    author="Brin Rosenthal (sbrosenthal@ucsd.edu), "
           "Mikayla Webster (m1webste@ucsd.edu), "
           "Aaron Gary (agary@ucsd.edu), "
           "Julia Len (jlen@ucsd.edu), "
           "Daniil Vodolazsky (daniil.vodolazsky@mail.ru)",
    author_email="sbrosenthal@ucsd.edu",
    keywords=['Jupyter notebook', 'interactive', 'network'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'networkx', 'numpy', 'scipy', 'IPython', 'matplotlib'
    ]
)
