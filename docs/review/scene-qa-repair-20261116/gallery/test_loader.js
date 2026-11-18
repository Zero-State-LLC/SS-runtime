'use strict';
// Synthetic DOM/network harness only. This is not browser or native-run evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const nodeCrypto = require('node:crypto');
const gallery = require('./gallery.js');

class Element {
  constructor() {
    this.children = [];
    this.dataset = {};
    this.handlers = {};
    this.classes = new Set();
    this.classList = { toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name) };
    this.hidden = false;
    this.textContent = '';
  }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  addEventListener(event, callback) { this.handlers[event] = callback; }
}
const ids = ['capture', 'controls', 'reload', 'captures', 'error', 'capture-label', 'evidence-links',
  'status', 'zoom', 'arm', 'size', 'grayscale', 'benchmark', 'records-link', 'verification-link', 'reference-error'];
const elements = Object.fromEntries(ids.map(id => [id, new Element()]));
Object.assign(elements.capture, { value: 'v6' });
const options = Object.fromEntries(['v4', 'v5', 'v6'].map(id => [id, new Element()]));
Object.defineProperty(elements.capture, 'selectedOptions', { get: () => [options[elements.capture.value]] });
Object.assign(elements.zoom, { value: '1' });
Object.assign(elements.arm, { value: 'paired' });
Object.assign(elements.size, { value: 'native' });
Object.assign(elements.grayscale, { checked: false });
Object.assign(elements.benchmark, { complete: true, naturalWidth: 1672 });
globalThis.document = {
  getElementById: id => elements[id],
  createElement: () => new Element(),
  createDocumentFragment: () => new Element()
};
if (!globalThis.crypto) Object.defineProperty(globalThis, 'crypto', { value: nodeCrypto.webcrypto });
const requests = [];
let responses = new Map();
globalThis.fetch = async (url, options) => {
  requests.push(url);
  assert.equal(options.cache, 'no-store');
  const bytes = responses.get(url);
  return { ok: Boolean(bytes), status: bytes ? 200 : 404,
    arrayBuffer: async () => Uint8Array.from(bytes).buffer };
};
const objectURLs = new Map();
const revoked = [];
let urlID = 0;
globalThis.URL = {
  createObjectURL(blob) { const url = `blob:synthetic-${++urlID}`; objectURLs.set(url, blob); return url; },
  revokeObjectURL(url) { revoked.push(url); objectURLs.delete(url); }
};
globalThis.Image = class {
  set src(url) {
    objectURLs.get(url).arrayBuffer().then(buffer => {
      const bytes = Buffer.from(buffer);
      this.naturalWidth = bytes.readUInt32BE(16);
      this.naturalHeight = bytes.readUInt32BE(20);
      this.onload();
    }).catch(() => this.onerror());
  }
};

function retainedResponses(id) {
  const root = gallery.captureConfig(id).root;
  const disk = path.resolve(__dirname, root);
  const recordBytes = fs.readFileSync(path.join(disk, 'source-scene-records.json'));
  const verificationBytes = fs.readFileSync(path.join(disk, 'verification.json'));
  const files = gallery.validateEvidence(JSON.parse(recordBytes), JSON.parse(verificationBytes), id);
  return new Map([
    [root + 'source-scene-records.json', recordBytes], [root + 'verification.json', verificationBytes],
    ...files.map(file => [root + file.name, fs.readFileSync(path.join(disk, file.name))])
  ]);
}
function descendants(element) {
  return element.children.flatMap(child => [child, ...descendants(child)]);
}
function visibleImages() { return descendants(elements.captures).filter(node => node.className === 'capture-image'); }
async function settled() {
  const deadline = Date.now() + 5000;
  while (elements.reload.disabled !== false) {
    assert.ok(Date.now() < deadline, 'Synthetic loader did not settle');
    await new Promise(resolve => setTimeout(resolve, 5));
  }
}
function assertPending(id) {
  assert.equal(elements.capture.value, id);
  assert.equal(elements.controls.disabled, true);
  assert.equal(visibleImages().length, 0);
  assert.equal(elements['capture-label'].textContent, '');
  assert.equal(elements['evidence-links'].hidden, true);
  assert.equal(elements.error.hidden, false);
  assert.match(elements.status.textContent, /pending or invalid evidence/);
  assert.match(elements.status.textContent, /No fallback to another capture/);
  if (id === 'v6') assert.equal(options.v6.textContent, gallery.captureConfig('v6').pendingLabel);
}
async function select(id) {
  elements.capture.value = id;
  await elements.capture.handlers.change();
  await settled();
}

async function main() {
  // Missing v6 must request only v6, leave controls disabled and display no capture.
  gallery.initGallery();
  await settled();
  assertPending('v6');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(gallery.captureConfig('v6').root)));
  assert.equal(objectURLs.size, 0);

  // Existing v5 still loads actual retained hashes and all eighteen actual PNGs.
  responses = retainedResponses('v5');
  await select('v5');
  assert.equal(elements.controls.disabled, false);
  assert.equal(objectURLs.size, 18);
  assert.equal(visibleImages().length, 2);
  let selections = 0;
  for (const zoom of ['1', '1.25', '1.4']) for (const arm of ['paired', 'control', 'candidate']) {
    for (const size of ['native', 'half']) for (const gray of [false, true]) {
      elements.zoom.value = zoom;
      elements.arm.value = arm;
      elements.size.value = size;
      elements.grayscale.checked = gray;
      elements.size.handlers.change();
      const images = visibleImages();
      assert.equal(images.length, arm === 'paired' ? 2 : 1);
      for (const image of images) {
        assert.equal(image.width, size === 'native' ? 704 : 352);
        assert.equal(image.height, size === 'native' ? 326 : 163);
        assert.match(image.dataset.evidenceFile, gray ? /-grayscale\.png$/ : size === 'half' ? /-half\.png$/ : /-native\.png$/);
      }
      assert.equal(elements.benchmark.classes.has('grayscale'), gray);
      selections++;
    }
  }

  // A v5 packet served at the v6 path cannot masquerade as v6 or leave v5 displayed.
  const v5Root = gallery.captureConfig('v5').root;
  const v6Root = gallery.captureConfig('v6').root;
  const v5 = responses;
  responses = new Map([...v5].map(([url, bytes]) => [url.replace(v5Root, v6Root), bytes]));
  requests.length = 0;
  await select('v6');
  assertPending('v6');
  assert.ok(requests.every(url => url.startsWith(v6Root)));
  assert.equal(requests.length, 2, 'Invalid fixture must fail before any PNG request');
  assert.equal(objectURLs.size, 0);
  assert.equal(revoked.length, 18, 'Switching away from v5 releases every old image URL');

  // Even when v5 is available, missing v6 is not replaced by it on reload.
  responses = v5;
  requests.length = 0;
  await elements.reload.handlers.click();
  await settled();
  assertPending('v6');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v6Root)));
  assert.equal(objectURLs.size, 0);
  // Virtual protocol packet only. Reuse retained pixels in memory to exercise v6
  // loading/hash failure mechanics, never write or publish fabricated native evidence.
  const virtual = new Map([...v5].map(([url, bytes]) => [url.replace(v5Root, v6Root), bytes]));
  const record = JSON.parse(virtual.get(v6Root + 'source-scene-records.json'));
  const verification = JSON.parse(virtual.get(v6Root + 'verification.json'));
  record.fixtureVersion = verification.fixtureVersion = gallery.captureConfig('v6').version;
  record.schema = gallery.captureConfig('v6').recordSchema;
  const recordBytes = Buffer.from(JSON.stringify(record));
  verification.files['source-scene-records.json'] = nodeCrypto.createHash('sha256').update(recordBytes).digest('hex');
  virtual.set(v6Root + 'source-scene-records.json', recordBytes);
  virtual.set(v6Root + 'verification.json', Buffer.from(JSON.stringify(verification)));
  responses = virtual;
  requests.length = 0;
  await select('v6');
  assert.equal(elements.controls.disabled, false);
  assert.equal(objectURLs.size, 18);
  assert.ok(elements['capture-label'].textContent.startsWith('Capture v6:'));
  assert.equal(options.v6.textContent, gallery.captureConfig('v6').verifiedLabel);
  assert.ok(requests.every(url => url.startsWith(v6Root)));

  // A single changed PNG byte must clear the valid prior display, not show v5.
  const firstPNG = v6Root + record.captures[0].name + '-native.png';
  const corrupt = Buffer.from(virtual.get(firstPNG));
  corrupt[corrupt.length - 1] ^= 1;
  responses = new Map([...v5, ...virtual, [firstPNG, corrupt]]);
  requests.length = 0;
  await select('v6');
  assertPending('v6');
  assert.match(elements.error.textContent, /PNG bytes differ from recorded hash/);
  assert.ok(requests.every(url => url.startsWith(v6Root)));
  assert.equal(objectURLs.size, 0);

  // Structurally valid record JSON still fails if its exact bytes are unbound.
  responses = new Map([...v5, ...virtual,
    [v6Root + 'source-scene-records.json', Buffer.concat([recordBytes, Buffer.from('\n')])]]);
  requests.length = 0;
  await select('v6');
  assertPending('v6');
  assert.match(elements.error.textContent, /Records bytes differ from importer hash/);
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v6Root)));
  console.log(JSON.stringify({ result: 'PASS', missingV6: true, mismatchedCaptureRejected: true,
    corruptedPNGRejected: true, corruptedRecordRejected: true, syntheticV6Only: true,
    noFallback: true, retainedV5Selections: selections, browserEvidence: false, nativeRun: false }));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
