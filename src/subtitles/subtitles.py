import logging
from dataclasses import dataclass
from typing import List
import whisper
import re

LOG = logging.getLogger(__name__)


@dataclass
class SubtitleSection:
    text: str
    start: float
    end: float


@dataclass
class SubtitleLine:
    sections: List[SubtitleSection]
    start: float
    end: float

    @property
    def text(self) -> str:
        return " ".join(section.text for section in self.sections)


def get_subtitle_words(audio_path: str) -> List[SubtitleSection]:
    LOG.info(f"Starting transcription of audio file: {audio_path}")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True, fp16=False)
    LOG.info("Transcription complete. Processing words...")

    sections = []
    for segment in result["segments"]:
        i = 0
        segment_words = segment["words"]
        num_of_words = len(segment_words)
        while i < num_of_words:
            word = segment_words[i]
            if (i + 1) < num_of_words:
                next_word = segment_words[i + 1]
                if next_word["word"].startswith("-"):
                    word["word"] += next_word["word"]
                    word["end"] = next_word["end"]
                    i += 1  # Skip the next word in the next iteration
                    LOG.debug(f"Combined hyphenated word: {word['word']}")
            sections.append(
                SubtitleSection(
                    text=format_word(word["word"]), start=word["start"], end=word["end"]
                )
            )
            i += 1

    LOG.info(f"Processed {len(sections)} words")
    return sections


def get_subtitle_lines(
    sections: List[SubtitleSection], max_chars: int = 13, lines_distance: float = 0.05
) -> List[SubtitleLine]:
    LOG.info(f"Grouping words into lines (max {max_chars} characters per line)")
    lines = []
    current_line = []
    line_text = ""

    for section in sections:
        line_text = f"{line_text} {section.text}".strip()

        if current_line and len(line_text) > max_chars:
            lines.append(
                SubtitleLine(
                    sections=current_line,
                    start=current_line[0].start,
                    end=current_line[-1].end,
                )
            )
            LOG.debug(f"Created line: {lines[-1].text}")
            if current_line[-1].end == section.start:
                section.start += lines_distance
                LOG.debug(f"Added time gap of {lines_distance}s")
            current_line = []
            line_text = section.text

        current_line.append(section)

    if current_line:
        lines.append(
            SubtitleLine(
                sections=current_line,
                start=current_line[0].start,
                end=current_line[-1].end,
            )
        )
        LOG.debug(f"Created final line: {lines[-1].text}")

    LOG.info(f"Created {len(lines)} subtitle lines")
    return lines


def format_word(word: str) -> str:
    formatted = re.sub(r"[;,.]", "", word).upper().strip()
    LOG.debug(f"Formatted word: '{word}' -> '{formatted}'")
    return formatted
