import setuptools

setuptools.setup(
    install_requires=open('requirements.txt').read().splitlines(),
    name="abba_model_f41",
    version="0.0.2",
    license="MIT",
    author="abba",
    author_email="jaebin9274@cogniterm.com",
    description="sample",
    long_description=open("README.md").read(),
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]    
)