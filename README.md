# Subtitles

This Python package uses the Whisper model to transcribe audio files and generate structured subtitles. It processes the transcription into word-level and line-level subtitle objects, allowing for flexible subtitle creation and manipulation.

## Description:

This Python package provides a comprehensive solution for generating structured subtitles from audio files using OpenAI's Whisper speech recognition model. The package offers the following key features:
- Audio Transcription: Utilizes the Whisper model to transcribe audio files with word-level timestamps.
- Subtitle Structuring: Organizes transcribed text into two levels of subtitle objects:
- SubtitleSection: Represents individual words or short phrases with start and end times.
- SubtitleLine: Groups multiple SubtitleSections into coherent lines of subtitles.
- Word Processing: Handles hyphenated words by combining them into single subtitle sections.
- Text Formatting: Applies uppercase formatting and removes certain punctuation from words.
- Line Generation: Creates subtitle lines based on a maximum character limit, ensuring readability.
- Timing Adjustment: Implements a small time gap between consecutive subtitle lines for better readability.
- Flexible Configuration: Allows customization of parameters such as maximum characters per line and time gap between lines.

This package is ideal for developers and content creators who need to generate accurate, well-structured subtitles for videos, podcasts, or any audio content. It provides a foundation for further subtitle processing, such as exporting to various subtitle formats or integrating with video editing software.

## How to install:

Run the following command in your python venv:

```sh
pip install git+https://github.com/avivilloz/subtitles.git@main#egg=subtitles
```

Or add the following line to your project's `requirement.txt` file:

```
git+https://github.com/avivilloz/subtitles.git@main#egg=subtitles
```

And run the following command:

```sh
pip install -r requirements.txt
```

## How to use:

```python
from subtitles import get_subtitle_words, get_subtitle_lines

# Specify the path to your audio file
audio_path = "path/to/your/audio/file.mp3"

# Get the subtitle sections (words)
sections = get_subtitle_words(audio_path)

# Generate subtitle lines from the sections (optional)
lines = get_subtitle_lines(sections, max_chars=30)

# Print the subtitle lines with their start and end times
for line in lines:
    print(f"{line.start:.2f} - {line.end:.2f}: {line.text}")
```