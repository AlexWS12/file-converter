from pathlib import Path
from pydub import AudioSegment


def wav_to_mp3(src: Path, dst: Path) -> None:
    """WAV → MP3 (192 kbps). Requires ffmpeg on PATH."""
    audio = AudioSegment.from_wav(str(src))
    audio.export(str(dst), format="mp3", bitrate="192k")


def mp3_to_wav(src: Path, dst: Path) -> None:
    """MP3 → WAV (PCM). Requires ffmpeg on PATH."""
    audio = AudioSegment.from_mp3(str(src))
    audio.export(str(dst), format="wav")
