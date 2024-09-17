import re
import logging
import whisper

__all__ = [
    "get_subtitles",
    "get_subtitle_lines",
    "get_words_from_segments",
]

LOG = logging.getLogger(__name__)


def get_subtitles(audio_path: str):
    LOG.info(f"Starting transcription of audio file: {audio_path}")
    model = whisper.load_model("base")
    segments = model.transcribe(audio_path, word_timestamps=True, fp16=False)
    LOG.info("Transcription complete.")
    return process_segments(segments=segments)


def process_segments(segments: list):
    LOG.info("Processing segments...")

    processed_segments = []
    for segment in segments["segments"]:
        new_segment = {
            "text": segment["text"],
            "start": segment["start"],
            "end": segment["end"],
            "words": [],
        }

        segment_words = segment["words"]
        num_of_words = len(segment_words)
        i = 0

        while i < num_of_words:
            word = segment_words[i]

            if (i + 1) < num_of_words:
                next_word = segment_words[i + 1]

                if next_word["word"].startswith("-"):
                    word["word"] += next_word["word"]
                    word["end"] = next_word["end"]

                    i += 1  # Skip the next word in the next iteration

                    LOG.debug(f"Combined hyphenated word: {word['word']}")

            new_segment["words"].append(
                {
                    "word": format_word(word["word"]),
                    "start": word["start"],
                    "end": word["end"],
                }
            )

            i += 1

        processed_segments.append(new_segment)

    LOG.info(f"Processed {len(processed_segments)} segments")

    return processed_segments


def get_subtitle_lines(
    segments: list, max_chars: int = 13, lines_distance: float = 0.05
):
    LOG.info(f"Grouping words into lines (max {max_chars} characters per line)")

    lines = []
    words = []
    line_text = ""

    for word in get_words_from_segments(segments=segments):
        current_word = {
            "word": word["word"],
            "start": word["start"],
            "end": word["end"],
        }

        word_text = current_word["word"]
        temp_line_text = f"{line_text} {word_text}".strip()

        if words and len(temp_line_text) > max_chars:
            lines.append(get_line(words=words, line_text=line_text))
            LOG.debug(f"Created line: {lines[-1]['text']}")

            if words[-1]["end"] == current_word["start"]:
                current_word["start"] += lines_distance
                LOG.debug(f"Added time gap of {lines_distance}s")

            words = []
            line_text = current_word["word"]
        else:
            line_text = temp_line_text

        words.append(current_word)

    if words:
        lines.append(get_line(words=words, line_text=line_text))
        LOG.debug(f"Created final line: {lines[-1]['text']}")

    LOG.info(f"Created {len(lines)} subtitle lines")

    return lines


def format_word(word: str) -> str:
    formatted = re.sub(r"[;,.]", "", word).upper().strip()
    LOG.debug(f"Formatted word: '{word}' -> '{formatted}'")
    return formatted


def get_line(words: list, line_text: str):
    return {
        "text": line_text,
        "start": words[0]["start"],
        "end": words[-1]["end"],
        "words": words,
    }


def get_words_from_segments(segments: list):
    return [word for segment in segments for word in segment["words"]]
