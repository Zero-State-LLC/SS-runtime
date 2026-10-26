"""Measure integer-pixel support-patch displacement in archived native stills.

Diagnostic only: not video tracking, subpixel accuracy, or contact acceptance.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat


def main():
    here = Path(__file__).resolve().parent
    captures = here.parents[4] / "outputs/SS-player-settle-clean-pose-review"
    inputs, observations = [], []
    for release, first_x in ((5, 275), (13, 300)):
        images = []
        for pose in range(17):
            path = captures / f"stop-{release:02d}-pose-{pose:02d}.png"
            image = Image.open(path).convert("RGB")
            if image.size != (576, 432):
                raise ValueError(f"Unexpected capture size: {path}")
            images.append(image)
            inputs.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        plate = Image.new("RGB", (1800, 1792), (35, 35, 35))
        draw = ImageDraw.Draw(plate)
        for pose, image in enumerate(images):
            x, y = pose % 5 * 360, pose // 5 * 448
            plate.paste(image.crop((245, 220, 335, 325)).resize((360, 420), Image.Resampling.NEAREST), (x, y))
            draw.text((x + 8, y + 425), f"release {release} pose {pose}", fill="white")
        plate.save(captures / f"stop-{release:02d}-foot-detail.png")

        # Fixed native-image patches selected from the inspected boot silhouettes.
        # Intervals come from the source proposal's toe-contact declarations.
        for start, end, cx, cy in ((1, 8, first_x, 263), (8, 16, 575 - first_x, 289)):
            box = (cx - 6, cy - 7, cx + 7, cy + 8)
            template = images[start].crop(box)
            for pose in range(start, end + 1):
                scores = []
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        candidate = images[pose].crop((box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy))
                        error = sum(ImageStat.Stat(ImageChops.difference(template, candidate)).mean) / 3
                        scores.append((error, dx, dy))
                scores.sort()
                observations.append({
                    "release": release, "pose": pose, "interval": [start, end],
                    "templateBox": box, "bestOffsetPixels": list(scores[0][1:]),
                    "meanAbsoluteRGBError": scores[0][0],
                    "runnerUpErrorMargin": scores[1][0] - scores[0][0],
                })
    result = {
        "scope": "archived static native captures; integer-pixel translation search only",
        "searchRadiusPixels": 3, "inputs": inputs, "observations": observations,
        "allBestOffsetsZero": all(row["bestOffsetPixels"] == [0, 0] for row in observations),
        "limitations": ["Not live cadence or physical screen evidence", "Not subpixel tracking", "Patches include background", "Toe stability does not prove heel or full-sole support"],
    }
    (here / "native-support-patches.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"{len(observations)} patch observations; all integer offsets zero: {result['allBestOffsetsZero']}")


if __name__ == "__main__":
    main()
