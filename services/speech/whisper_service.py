from faster_whisper import WhisperModel
import tempfile
import os


class WhisperService:

    def __init__(self):

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_bytes):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as f:

            f.write(audio_bytes)
            audio_path = f.name

        segments, info = self.model.transcribe(
            audio_path
        )

        text = " ".join(
            segment.text
            for segment in segments
        )

        os.remove(audio_path)

        return text.strip()