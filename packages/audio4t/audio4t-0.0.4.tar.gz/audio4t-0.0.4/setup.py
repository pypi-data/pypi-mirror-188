import setuptools

# with open("README.md", "r",encoding="utf8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="audio4t",
    version="0.0.4",
    author="Wen-Hung, Chang 張文宏",
    author_email="beardad1975@nmes.tyc.edu.tw",
    description="Audio learning wrapper library for Teenagers",
    long_description="Audio learning wrapper library for Teenagers",
    long_description_content_type="text/markdown",
    url="https://github.com/beardad1975/audio4t",
    #packages=setuptools.find_packages(),
    platforms=["Windows"],
    python_requires=">=3.8",
    packages=['audio4t','聲音模組'],
    install_requires = ['pyaudio == 0.2.13','pydub == 0.25.1', 'simpleaudio == 1.0.4'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            #"Operating System :: MacOS",
            #"Operating System :: POSIX :: Linux",
            "Natural Language :: Chinese (Traditional)",
        ],
)