"""Source-level wiring guards, NOT Swift compilation or native behavior tests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def source(name):
    return (ROOT / name).read_text()

class RuntimeAuditGuards(unittest.TestCase):
    def test_pause_has_one_composed_owner(self):
        scene = source('App/GameScene.swift')
        self.assertNotIn('renderer.root.isPaused = paused', scene)
        self.assertIn('vfx.setRunPaused(paused)', scene)
        vfx = source('App/VFXRenderer.swift')
        self.assertIn('runPaused || frozen', vfx)
        self.assertIn('cameraNode?.position = cameraBase', vfx)

    def test_preferences_cleanup_at_assignment(self):
        vfx = source('App/VFXRenderer.swift')
        self.assertIn('didSet', vfx)
        self.assertIn('settings.reducedMotion && !oldValue.reducedMotion', vfx)
        self.assertIn('settings.reducedFlash && !oldValue.reducedFlash', vfx)
        self.assertIn('clearTransientEffects()', vfx)

    def test_audio_pause_cancels_deferred_work(self):
        audio = source('App/AudioEngine.swift')
        self.assertIn('func setSuspended', audio)
        self.assertIn('soundEngine.setSuspended(paused)', source('App/GameScene.swift'))
        self.assertIn('dropTask?.cancel()', audio)
        self.assertIn('cueTasks', audio)
        self.assertIn('!interrupted, !suspended', audio)

    def test_effects_share_priority_pool(self):
        audio = source('App/AudioEngine.swift')
        self.assertNotIn('voiceCursor', audio)
        self.assertIn('effectPool.admit(priority: cue.priority', audio)
        self.assertIn('effectPool.stopAll()', audio)
        pitched = source('App/PitchedVoice.swift')
        self.assertIn('engine.stop()', pitched.split('func stop()')[1])

    def test_asset_guard_fails_closed(self):
        registry = source('App/RuntimeAssetRegistry.swift')
        self.assertNotIn('?? assetId', registry)
        self.assertNotIn('try!', registry)
        self.assertIn('return unavailable', registry)
        self.assertIn('diagnose(', registry)

if __name__ == '__main__':
    unittest.main()
