from setuptools import setup, find_packages

setup(
    name="sismodata",
    version="0.1.0",
    description="Paquete para descargar y procesar datos de sismos desde el IGP de Perú",
    author="Jhon K. Flores Rojas",
    author_email="fr.jhonk@gmail.com",
    url="https://github.com/tjhon/sismodata",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.1.5",
        "openpyxl>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    license="Apache License 2.0",
)
