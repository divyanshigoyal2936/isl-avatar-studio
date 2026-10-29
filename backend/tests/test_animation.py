import unittest
from app.services.animation_service import animation_service

class TestAnimationService(unittest.TestCase):
    def test_manifest_contains_verified_signs(self):
        manifest = animation_service.get_manifest()
        self.assertGreaterEqual(manifest["total_verified_signs"], 20)

    def test_schedule_verified_tokens(self):
        clips, supported, unsupported, cov, total_dur, warnings = animation_service.schedule_sequence(
            ["HELLO", "THANK-YOU", "WATER"]
        )
        self.assertEqual(len(clips), 3)
        self.assertEqual(len(supported), 3)
        self.assertEqual(len(unsupported), 0)
        self.assertEqual(cov, 100.0)
        self.assertGreater(total_dur, 2000)
        self.assertEqual(len(warnings), 0)

        # Check time continuity
        for i in range(len(clips) - 1):
            self.assertLess(clips[i].start_time_ms, clips[i+1].start_time_ms)
            self.assertLessEqual(clips[i].end_time_ms, clips[i+1].start_time_ms)

    def test_alias_resolution(self):
        # NAMASTE should resolve to HELLO
        clips, supported, _, _, _, _ = animation_service.schedule_sequence(["NAMASTE"])
        self.assertIn("HELLO", supported)
        self.assertEqual(clips[0].gloss_token, "HELLO")

    def test_unsupported_token_transparent_fallback(self):
        clips, supported, unsupported, cov, total_dur, warnings = animation_service.schedule_sequence(
            ["WATER", "UNOBTAINIUM_XYZ"]
        )
        self.assertIn("WATER", supported)
        self.assertIn("UNOBTAINIUM_XYZ", unsupported)
        self.assertEqual(cov, 50.0)
        self.assertEqual(len(warnings), 1)
        self.assertFalse(clips[1].is_verified)
        self.assertIn("not yet certified", clips[1].description)

if __name__ == "__main__":
    unittest.main()
