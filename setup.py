from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    "numpy",
    "scipy",
    "scikit-image",
    "tqdm",
    "fire",
    "pyproj"
]


setup(name='earthnet', 
        version='0.2.2',
        description="EarthNet2021 Toolkit: Download, Evaluation, Plotting",
        author="Vitus Benson",
        author_email="vbenson@bgc-jena.mpg.de",
        url="https://earthnet.tech",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
                "Intended Audience :: Science/Research",
                "License :: Other/Proprietary License",
                "Programming Language :: Python :: 3"
                 ],
        packages=find_packages(),
        install_requires=install_requires,
        )
