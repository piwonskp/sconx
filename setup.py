import setuptools

setuptools.setup(
    name="sconx",
    version="0.0.1",
    author="Piotr Piwoński",
    description="Low latency requests powered by connexion",
    url="https://github.com/piwonskp/sconx",
    packages=setuptools.find_packages(),
    install_requires=["connexion>=2.6.0"],
)
