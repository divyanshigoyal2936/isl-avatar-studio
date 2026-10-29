import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from app.core.config import settings
from app.models.schemas import ScheduledClip

logger = logging.getLogger("AnimationService")

class AnimationService:
    def __init__(self):
        self.manifest_path = Path(settings.ANIMATION_MANIFEST_PATH)
        self.manifest: Dict[str, Any] = {}
        self.alias_map: Dict[str, str] = {}
        self._load_manifest()

    def _load_manifest(self):
        if not self.manifest_path.exists():
            logger.warning(f"Animation manifest not found at {self.manifest_path}")
            return

        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.manifest = data.get("signs", {})
                
            # Build alias map
            for gloss_id, sign_meta in self.manifest.items():
                self.alias_map[gloss_id.upper()] = gloss_id
                for alias in sign_meta.get("aliases", []):
                    self.alias_map[alias.upper()] = gloss_id
            logger.info(f"Loaded {len(self.manifest)} verified sign animations into library.")
        except Exception as e:
            logger.error(f"Error loading animation manifest: {e}")

    def schedule_sequence(self, gloss_tokens: List[str]) -> Tuple[List[ScheduledClip], List[str], List[str], float, int, List[str]]:
        """
        Schedules a time-ordered sequence of 3D sign clips with transitions and non-manual markers.
        Returns:
            (scheduled_clips, supported_tokens, unsupported_tokens, coverage_pct, total_duration_ms, warnings)
        """
        scheduled_clips: List[ScheduledClip] = []
        supported: List[str] = []
        unsupported: List[str] = []
        warnings: List[str] = []

        current_time_ms = 300  # Initial rest pause before signing begins

        for idx, token in enumerate(gloss_tokens):
            norm_token = token.upper()
            resolved_id = self.alias_map.get(norm_token)

            if resolved_id and resolved_id in self.manifest:
                meta = self.manifest[resolved_id]
                duration = meta.get("duration_ms", 1000)
                trans_in = meta.get("transition_in_ms", 150)
                trans_out = meta.get("transition_out_ms", 150)

                clip = ScheduledClip(
                    clip_id=f"clip_{idx}_{resolved_id}",
                    gloss_token=resolved_id,
                    start_time_ms=current_time_ms,
                    duration_ms=duration,
                    end_time_ms=current_time_ms + duration,
                    transition_in_ms=trans_in,
                    transition_out_ms=trans_out,
                    hand_dominance=meta.get("hand_dominance", "dominant_only"),
                    hand_shape=meta.get("hand_shape", "OPEN_FLAT"),
                    palm_orientation=meta.get("palm_orientation", "INWARD"),
                    signing_space=meta.get("signing_space", "CHEST_CENTER"),
                    movement_type=meta.get("movement_type", "HOLD"),
                    non_manual_markers=meta.get("non_manual_markers", {"eyebrow": "NEUTRAL", "head": "NEUTRAL", "mouth": "NEUTRAL"}),
                    is_verified=True,
                    joint_targets=meta.get("joint_targets"),
                    description=meta.get("description")
                )
                scheduled_clips.append(clip)
                supported.append(resolved_id)
                current_time_ms += duration + 100  # 100ms inter-sign spacing
            else:
                # Unsupported token: transparent fallback without fake sign
                fallback_duration = 900
                clip = ScheduledClip(
                    clip_id=f"clip_{idx}_{norm_token}_unsupported",
                    gloss_token=norm_token,
                    start_time_ms=current_time_ms,
                    duration_ms=fallback_duration,
                    end_time_ms=current_time_ms + fallback_duration,
                    transition_in_ms=100,
                    transition_out_ms=100,
                    hand_dominance="dominant_only",
                    hand_shape="INDEX_1",
                    palm_orientation="FORWARD",
                    signing_space="NEUTRAL_SPACE",
                    movement_type="HOLD",
                    non_manual_markers={"eyebrow": "NEUTRAL", "head": "NEUTRAL", "mouth": "NEUTRAL"},
                    is_verified=False,
                    joint_targets=None,
                    description=f"Sign animation for '{norm_token}' is not yet certified in the ISL motion library."
                )
                scheduled_clips.append(clip)
                unsupported.append(norm_token)
                warnings.append(f"Gloss token '{norm_token}' lacks a certified 3D motion clip; textual explanation and fingerspelling fallback provided.")
                current_time_ms += fallback_duration + 100

        total_tokens = len(gloss_tokens)
        coverage_pct = round((len(supported) / total_tokens * 100), 1) if total_tokens > 0 else 0.0
        total_duration = current_time_ms + 300  # Final rest return

        return scheduled_clips, supported, unsupported, coverage_pct, total_duration, warnings

    def get_sign(self, gloss_id: str) -> Optional[Dict[str, Any]]:
        norm_id = gloss_id.upper()
        resolved = self.alias_map.get(norm_id)
        if resolved and resolved in self.manifest:
            return self.manifest[resolved]
        return None

    def get_manifest(self) -> Dict[str, Any]:
        return {
            "total_verified_signs": len(self.manifest),
            "signs": self.manifest
        }

animation_service = AnimationService()
