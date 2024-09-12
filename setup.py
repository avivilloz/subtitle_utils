from setuptools import setup, find_packages

setup(
    name="easysub",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "whisper",
        "openai-whisper",
    ],
    author="Aviv Illoz",
    author_email="avivilloz@gmail.com",
    description=(
        "Transcribes audio files and generate structured subtitles. It "
        "processes the transcription into word-level and line-level subtitle "
        "objects, allowing for flexible subtitle creation and manipulation."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avivilloz/easysub",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
