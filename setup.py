from setuptools import setup, find_packages

setup(
    name="djwsbridge",
    version="0.1.0",
    description="Real-time WebSocket bridge for Django (using Channels)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Asadbek",
    author_email="email@asadbektuygunov9@gmail.com",
    url="https://github.com/asadbek000002/djwsbridge",  # bo‘sh qoldirsa ham bo‘ladi
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Django>=4.0",
        "channels>=4.0",
        "asgiref>=3.5",
        "channels_redis>=4.0",
        "daphne>=4.0"
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
