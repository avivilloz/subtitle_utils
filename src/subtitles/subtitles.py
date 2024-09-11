from dataclasses import dataclass
from typing import List
import whisper
import re


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
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True, fp16=False)

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
            sections.append(
                SubtitleSection(
                    text=format_word(word["word"]), start=word["start"], end=word["end"]
                )
            )
            i += 1

    return sections


def get_subtitle_lines(
    sections: List[SubtitleSection], max_chars: int = 13, lines_distance: float = 0.05
) -> List[SubtitleLine]:
    lines = []
    current_line = []
    line_text = ""

    for section in sections:
        temp_line_text = f"{line_text} {section.text}".strip()

        if len(temp_line_text) > max_chars and current_line:
            lines.append(
                SubtitleLine(
                    sections=current_line,
                    start=current_line[0].start,
                    end=current_line[-1].end,
                )
            )
            if current_line[-1].end == section.start:
                section.start += lines_distance
            current_line = []
            line_text = ""

        current_line.append(section)
        line_text = temp_line_text

    if current_line:
        lines.append(
            SubtitleLine(
                sections=current_line,
                start=current_line[0].start,
                end=current_line[-1].end,
            )
        )

    return lines


def format_word(word: str) -> str:
    return re.sub(r"[;,.]", "", word).upper()


# Example usage
if __name__ == "__main__":
    audio_path = "/home/deck/git/subtitles/audio.wav"
    sections = get_subtitle_words(audio_path)
    lines = get_subtitle_lines(sections)

    for line in lines:
        print(f"{line.start:.2f} - {line.end:.2f}: {line.text}")
