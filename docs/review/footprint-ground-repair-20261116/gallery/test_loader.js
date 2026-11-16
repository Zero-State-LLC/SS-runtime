'use strict';
// Synthetic DOM/network harness only. This is not browser or native-run evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const nodeCrypto = require('node:crypto');
const gallery = require('./gallery.js');
const {packet,sha,clone,syntheticV8} = require('./test_helpers.js');

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
assert.equal(gallery.DEFAULT_CAPTURE, 'v8');
Object.assign(elements.capture, { value: gallery.DEFAULT_CAPTURE });
const options = Object.fromEntries(['v7', 'v8'].map(id => [id, new Element()]));
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
  return packet(id).map;
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
  assert.equal(options[id].textContent, gallery.captureConfig(id).pendingLabel);
}
async function select(id) {
  elements.capture.value = id;
  await elements.capture.handlers.change();
  await settled();
}

async function main() {
  gallery.initGallery();
  await settled();
  assertPending('v8');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(gallery.captureConfig('v8').root)));
  assert.equal(objectURLs.size, 0);
  let selections = 0, versions = 0;
  const ids = ['v7'];
  if (fs.existsSync(path.resolve(__dirname, gallery.captureConfig('v8').root, 'verification.json'))) ids.push('v8');
  else assert.ok(!process.argv.includes('--require-v8'), 'Actual v8 evidence required');
  const actualVersions = ids.length;
  for (const entry of [...ids.map(id => ({id,map:retainedResponses(id)})),{id:'v8',map:syntheticV8().map,synthetic:true}]) {
    const id = entry.id;
    responses = entry.map;
    await select(id);
    assert.equal(elements.controls.disabled, false);
    assert.equal(objectURLs.size, 18);
    assert.equal(options[id].textContent, gallery.captureConfig(id).verifiedLabel);
    for (const zoom of ['1', '1.25', '1.4']) for (const arm of ['paired', 'baseline', 'candidate']) {
      for (const size of ['native', 'half']) for (const gray of [false, true]) {
        elements.zoom.value = zoom; elements.arm.value = arm;
        elements.size.value = size; elements.grayscale.checked = gray;
        elements.size.handlers.change();
        const images = visibleImages();
        assert.equal(images.length, arm === 'paired' ? 2 : 1);
        for (const image of images) {
          assert.equal(image.width, size === 'native' ? 704 : 352);
          assert.equal(image.height, size === 'native' ? 326 : 163);
          assert.match(image.dataset.evidenceFile, gray ? /-grayscale\.png$/ : size === 'half' ? /-half\.png$/ : /-native\.png$/);
        }
        assert.equal(elements.benchmark.classes.has('grayscale'), gray);
        if (id === 'v8') {
          const captions = descendants(elements.captures).filter(node => /logical CSS px/.test(node.textContent));
          assert.equal(captions.length,images.length);
          assert.ok(captions.every(c => /^(baselineV7|candidateV8) ·/.test(c.textContent)));
          if (arm !== 'paired') assert.ok(captions.every(c => c.textContent.startsWith(arm === 'baseline' ? 'baselineV7' : 'candidateV8')));
        }
        selections++;
      }
    }
    const root = gallery.captureConfig(id).root;
    const valid = responses;
    const recordBytes = valid.get(root + 'source-scene-records.json');
    const record = JSON.parse(recordBytes);
    const firstPNG = root + record.captures[0].name + '-native.png';
    const corrupt = Buffer.from(valid.get(firstPNG)); corrupt[corrupt.length - 1] ^= 1;
    responses = new Map([...valid, [firstPNG, corrupt]]);
    await select(id); assertPending(id);
    assert.match(elements.error.textContent, /PNG bytes differ/);
    assert.equal(objectURLs.size, 0);
    responses = new Map([...valid, [root + 'source-scene-records.json', Buffer.concat([recordBytes, Buffer.from('\n')])]]);
    await select(id); assertPending(id);
    assert.match(elements.error.textContent, /Records bytes differ/);
    assert.equal(objectURLs.size, 0);
    // Every evidence dependency is mandatory, including each of all eighteen images.
    for (const missing of valid.keys()) {
      responses = new Map(valid); responses.delete(missing);
      await select(id); assertPending(id); assert.equal(objectURLs.size,0);
    }
    const sourceURL = [...valid.keys()].find(url => url.startsWith('../../../../docs/'));
    responses = new Map(valid); responses.set(sourceURL,Buffer.from('SYNTHETIC corrupted source'));
    await select(id); assertPending(id); assert.match(elements.error.textContent,/Source bytes differ/);
    const forged = clone(JSON.parse(valid.get(root + 'verification.json')));
    forged.testExecutable.expectedBuildSHA256 = '0'.repeat(64);
    responses = new Map(valid); responses.set(root + 'verification.json',Buffer.from(JSON.stringify(forged)));
    await select(id); assertPending(id); assert.match(elements.error.textContent,/executable binding/);
    const forgedRecord = clone(record), forgedVerification = clone(JSON.parse(valid.get(root + 'verification.json')));
    // Change innocuous V7 metadata so its byte pin, not shape checks, rejects it.
    if (id === 'v7') forgedRecord.forgedMetadata = true;
    else {
      forgedRecord.loadedTestExecutable.sha256 = packet('v7').record.loadedTestExecutable.sha256;
      forgedVerification.testExecutable.loadedSHA256 = forgedVerification.testExecutable.expectedBuildSHA256 = forgedRecord.loadedTestExecutable.sha256;
    }
    const forgedBytes = Buffer.from(JSON.stringify(forgedRecord));
    forgedVerification.files['source-scene-records.json'] = sha(forgedBytes);
    responses = new Map(valid);
    responses.set(root + 'source-scene-records.json',forgedBytes);
    responses.set(root + 'verification.json',Buffer.from(JSON.stringify(forgedVerification)));
    await select(id); assertPending(id);
    assert.match(elements.error.textContent,id === 'v7' ? /Immutable V7 records differ/ : /Stale V7 executable/);
    versions++;
  }
  const v7 = retainedResponses('v7'), v7Root = gallery.captureConfig('v7').root, v8Root = gallery.captureConfig('v8').root;
  responses = new Map([...v7].map(([url, bytes]) => [url.replace(v7Root, v8Root), bytes]));
  requests.length = 0;
  await select('v8'); assertPending('v8');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v8Root)));
  assert.equal(objectURLs.size, 0);
  responses = v7; requests.length = 0;
  await elements.reload.handlers.click(); await settled(); assertPending('v8');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v8Root)));
  console.log(JSON.stringify({result:'PASS',missingV8:true,mismatchedCaptureRejected:true,corruptedPNGRejected:true,corruptedRecordRejected:true,missingDependenciesRejected:true,sourceForgeryRejected:true,binaryForgeryRejected:true,noFallback:true,actualVersions,syntheticV8Loader:true,selections,browserEvidence:false,nativeRun:false}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
