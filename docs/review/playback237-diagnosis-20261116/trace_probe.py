"""Read retained post-action observations, never infer unseen displayed poses."""
import argparse
import json
from pathlib import Path


def diagnose(records):
    if not records:
        raise ValueError('empty trace')
    observed = set()
    gaps = []
    for row in records:
        frame = row['frame']
        if not isinstance(frame, int) or not -1 <= frame < 16:
            raise ValueError('invalid observed frame')
        if frame >= 0:
            observed.add(frame)
    for before, after in zip(records, records[1:]):
        left, right = before['clockSample'], after['clockSample']
        dt = right['spriteKitTime'] - left['spriteKitTime']
        entry_dt = right['updateEntryUptime'] - left['updateEntryUptime']
        if dt < 0 or entry_dt < 0:
            raise ValueError('nonmonotonic clock')
        if dt > 1 / 32:
            previous_work = before['updateStageSeconds']['total']
            gaps.append(dict(
                fromTick=before['tick'], toTick=after['tick'],
                fromFrame=before['frame'], toFrame=after['frame'],
                spriteKitDelta=dt, entryDelta=entry_dt,
                previousUpdateSeconds=previous_work,
                currentUpdateSeconds=after['updateStageSeconds']['total'],
                outsidePreviousUpdateSeconds=entry_dt - previous_work))
    return dict(recordCount=len(records), observed=sorted(observed),
                missing=sorted(set(range(16)) - observed), gaps=gaps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('--require-all-poses', action='store_true',
                        help='Return1 when any actual post-action pose is absent')
    args = parser.parse_args()
    result = diagnose(json.loads(args.trace.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(args.require_all_poses and bool(result['missing']))


if __name__ == '__main__':
    raise SystemExit(main())
