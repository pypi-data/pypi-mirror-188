from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Pacotes do Google Driver'
LONG_DESCRIPTION = 'Manipulação de arquivos com o Google Driver'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="modulozaz", 
        version=VERSION,
        author="Ivan Augusto de Azevedo",
        author_email="i.a.azevedo@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pydrive2'], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)