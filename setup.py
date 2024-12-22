from setuptools import setup, find_packages

setup(
    name='qrs-api-client',
    version='2.1.0',
    packages=find_packages(exclude=["examples", "docs"]),
    url='https://github.com/rumen-vasilev/qrs-api-client',
    license='Apache 2.0',
    author='Rumen Vasilev',
    author_email='rumen.vasilev@gmail.com',
    description='Python client for Qlik Sense Repository Service API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.32.3",
        "requests_ntlm>=1.2.0",
        "python-dotenv>=1.0.0"
    ],
    python_requires='>=3.6',
)
