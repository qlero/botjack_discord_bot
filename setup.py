import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botjack_discord_bot",
    version="0.1",
    author="LMquentinLR",
    description="Discord bot implementation with an ML-trained image classification function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
	url = "https://github.com/LMquentinLR/botjack_discord_bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
)