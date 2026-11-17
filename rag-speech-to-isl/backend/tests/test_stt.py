import unittest
from app.services.stt_service import FallbackSTTProvider, WhisperSTTProvider

class TestSTTService(unittest.TestCase):
    def setUp(self):
        self.fallback = FallbackSTTProvider()
        self.whisper_stt = WhisperSTTProvider()

    def test_empty_audio_raises_error(self):
        with self.assertRaises(ValueError):
            self.fallback.transcribe(b"", "test.wav")

    def test_too_brief_audio_raises_error(self):
        tiny_audio = b"RIFF" + b"\x00" * 20
        with self.assertRaises(ValueError):
            self.fallback.transcribe(tiny_audio, "test.wav")

    def test_valid_audio_fallback_transcription(self):
        # 1 second of 16kHz 16-bit mono PCM is ~32000 bytes
        mock_pcm = b"\x00" * 32000
        transcript, lang, conf, dur = self.fallback.transcribe(mock_pcm, "test.wav", language_hint="hi")
        self.assertIsNotNone(transcript)
        self.assertEqual(lang, "hi")
        self.assertGreaterEqual(conf, 0.8)
        self.assertGreaterEqual(dur, 0.5)

    def test_audio_size_limit(self):
        huge_bytes = b"0" * (16 * 1024 * 1024)
        with self.assertRaises(ValueError):
            self.whisper_stt.transcribe(huge_bytes, "huge.wav")

if __name__ == "__main__":
    unittest.main()
