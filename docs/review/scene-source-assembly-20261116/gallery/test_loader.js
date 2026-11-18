'use strict';
// Offline DOM/network doubles exercise the real loader, not a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const gallery = require('./gallery.js');
const historicalRoot = path.resolve(__dirname, gallery.captureConfig('1020').root);
const historical = JSON.parse(fs.readFileSync(path.join(historicalRoot, 'source-scene-records.json')));
const verified = JSON.parse(fs.readFileSync(path.join(historicalRoot, 'verification.json')));
assert.equal(gallery.DEFAULT_CAPTURE, '1040');
assert.throws(() => gallery.validateEvidence(historical, verified), /Wrong fixture version/);
for (const invalid of ['9999', '../1020', 'toString', '__proto__']) assert.throws(() => gallery.captureConfig(invalid));

function node() {
  return { value: '', checked: false, hidden: false, disabled: false, textContent: '', children: [], dataset: {}, handlers: {},
    classList: { toggle() {} }, append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    addEventListener(event, handler) { this.handlers[event] = handler; } };
}
async function main() {
  const elements = new Map();
  const get = id => { if (!elements.has(id)) elements.set(id, node()); return elements.get(id); };
  for (const [id, value] of Object.entries({capture:'1040', zoom:'1', arm:'paired', size:'native'})) get(id).value = value;
  const requests = [];
  const blobs = new Map();
  let sequence = 0;
  let mode = 'missing1040';
  const context = {
    console, TextDecoder, Blob, setTimeout, clearTimeout, crypto: crypto.webcrypto,
    document: {getElementById:get, createElement:node, createDocumentFragment:node},
    URL: {createObjectURL(blob) { const key = 'blob:' + ++sequence; blobs.set(key, blob); return key; }, revokeObjectURL(key) { blobs.delete(key); }},
    Image: class { set src(url) { blobs.get(url).arrayBuffer().then(bytes => { const png = Buffer.from(bytes); this.naturalWidth = png.readUInt32BE(16); this.naturalHeight = png.readUInt32BE(20); this.onload(); }); } },
    fetch: async url => {
      requests.push(url);
      if (url.includes('1040') && mode === 'missing1040') return {ok:false, status:404};
      const target = mode === 'wrongVersion' ? path.join(historicalRoot, path.basename(url)) : path.resolve(__dirname, url);
      if (!fs.existsSync(target)) return {ok:false, status:404};
      const bytes = fs.readFileSync(target);
      return {ok:true, arrayBuffer:async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)};
    }
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'gallery.js'), 'utf8'), context);
  async function settled() {
    const until = Date.now() + 10000;
    while (get('reload').disabled) {
      assert.ok(Date.now() < until, 'Offline loader timed out');
      await new Promise(resolve => setTimeout(resolve, 5));
    }
  }
  function closed() {
    assert.equal(get('controls').disabled, true);
    assert.equal(get('captures').children.length, 0);
    assert.equal(get('capture-label').textContent, '');
    assert.equal(get('evidence-links').hidden, true);
    assert.equal(get('error').hidden, false);
  }
  await settled(); closed();
  assert.ok(requests.every(url => url.startsWith('../native-capture-1040/')));
  get('capture').value = '1020'; await get('capture').handlers.change();
  assert.equal(get('controls').disabled, false);
  assert.equal(get('capture-label').textContent, 'Capture 1020: historical visual failure: issue247');
  assert.equal(get('captures').children[0].children.length, 2);
  get('capture').value = '1030'; await get('capture').handlers.change();
  assert.equal(get('controls').disabled, false);
  assert.equal(get('capture-label').textContent, 'Capture 1030: historical visual failure: issue248');
  get('capture').value = '1040';
  const pending = get('capture').handlers.change();
  assert.equal(get('captures').children.length, 0);
  await pending; closed();
  mode = 'wrongVersion'; await get('capture').handlers.change(); closed();
  assert.match(get('error').textContent, /Wrong fixture version/);
  get('capture').value = 'invalid'; await get('capture').handlers.change(); closed();
  // A stale historical request must not repaint after an invalid selection.
  mode = 'real'; get('capture').value = '1020'; const stale = get('capture').handlers.change();
  get('capture').value = 'invalid'; await get('capture').handlers.change(); await stale; closed();
  let corrected = 'PENDING: real 1040 packet absent, not certified';
  const correctedRoot = path.resolve(__dirname, gallery.captureConfig('1040').root);
  if (fs.existsSync(correctedRoot)) {
    get('capture').value = '1040'; await get('capture').handlers.change();
    assert.equal(get('error').hidden, true, get('error').textContent);
    assert.equal(get('controls').disabled, false);
    assert.equal(get('capture-label').textContent, 'Capture 1040: corrected harness, owner acceptance not granted');
    corrected = 'PASS: real 1040 records and all eighteen PNG hashes/dimensions';
  }
  console.log(JSON.stringify({offlineLoader:'PASS', missing1040:'fail closed, no fallback', historical1020and1030:'real evidence verified with issue247/248 labels', invalidSwitching:'rejected, stale loads isolated', corrected1040:corrected, browserEvidence:false}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
