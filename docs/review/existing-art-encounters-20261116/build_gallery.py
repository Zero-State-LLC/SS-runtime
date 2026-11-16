"""Build a self-contained gallery only after exact native evidence validation."""
import argparse
import base64
from html import escape
import json
from pathlib import Path
import subprocess

import verify_capture as v


def query_result(xcresult, kind):
    return json.loads(subprocess.check_output([
        'xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(xcresult)]))


def load_verified(exports, xcresult, query=query_result):
    v.validate_result(query(xcresult, 'summary'), query(xcresult, 'tests'))
    files = v.attachments(exports)
    packet = v.load(files['existing-art-encounter-records'])
    v.validate_packet(packet, files)
    return packet, files


def render(packet, files):
    # Defense in depth if callers retain a ledger then mutate an imported image.
    figures = []
    for row in packet['captures']:
        data = files[row['image']].read_bytes()
        v.need(v.sha(data) == row['pngSHA256'], 'Gallery image differs from validated ledger')
        width, height = row['sceneWidth'], row['sceneHeight']
        v.need(isinstance(width, (int, float)) and isinstance(height, (int, float))
               and 0 < width <= 8192 and 0 < height <= 8192, 'Invalid logical dimensions')
        label = escape(f"Tick {row['tick']} | tags: {', '.join(row['tags'])}")
        uri = 'data:image/png;base64,' + base64.b64encode(data).decode('ascii')
        views = []
        for scale, title in [(1, 'Native logical size'), (0.5, 'Half logical size')]:
            views.append(f'<h3>{title}: {width * scale:g} × {height * scale:g}</h3>'
                         f'<img alt="{label}" width="{width * scale:g}" height="{height * scale:g}" src="{uri}">')
        figures.append(f'<section><h2>{label}</h2><p>PNG pixels: {row["width"]} × {row["height"]}; '
                       f'SHA256: {escape(row["pngSHA256"])}</p>{"".join(views)}</section>')
    observed = escape(', '.join(packet['observed']) or 'none')
    missing = escape(', '.join(packet['notObserved']) or 'none')
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Existing-art encounter diagnostic</title><style>'
            'body{font:16px system-ui;margin:24px;background:#eee;color:#111}'
            '.warning{border:4px solid #a30;padding:16px;font-weight:bold;background:#fff2df}'
            'section{border-top:2px solid #555;margin-top:24px;overflow:auto}'
            'img{display:block;max-width:none;image-rendering:auto}p{overflow-wrap:anywhere}'
            'body:has(#gray:checked) img{filter:grayscale(1)}</style>'
            '<h1>Existing-art encounter diagnostic</h1><p class="warning">'
            'PRODUCTION-PROJECTION EXISTING-ART CONTROL. NOT A COHERENT BENCHMARK. '
            'STAGED SNAPSHOT PLAYER-CENTER FRAMING, NOT LIVE CAMERA FOLLOW. '
            'Source fidelity BLOCKED. Owner acceptance and production admission NOT GRANTED. '
            'Static captures do not establish live animation, cadence, or complete combat coverage.</p>'
            f'<p>Observed: {observed}</p><p>Not observed: {missing}</p>'
            '<label><input id="gray" type="checkbox"> Grayscale inspection (display only)</label>'
            + ''.join(figures) + '</html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    parser.add_argument('xcresult', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    packet, files = load_verified(args.exports, args.xcresult)
    html = render(packet, files)
    # Never replace an earlier review or failed attempt's output.
    with args.output.open('x') as output:
        output.write(html)
    print(f'Wrote {args.output}: {len(packet["captures"])} verified captures, not acceptance')


if __name__ == '__main__':
    main()
