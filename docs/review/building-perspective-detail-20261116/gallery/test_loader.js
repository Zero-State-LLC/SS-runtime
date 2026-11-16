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
Object.assign(elements.capture, { value: 'v7' });
const options = Object.fromEntries(['v6', 'v7'].map(id => [id, new Element()]));
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
  assertPending('v7');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(gallery.captureConfig('v7').root)));
  assert.equal(objectURLs.size, 0);
  let selections = 0, versions = 0;
  const ids = ['v6'];
  if (fs.existsSync(path.resolve(__dirname, gallery.captureConfig('v7').root, 'verification.json'))) ids.push('v7');
  else assert.ok(!process.argv.includes('--require-v7'), 'Actual v7 evidence required');
  for (const id of ids) {
    responses = retainedResponses(id);
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
    versions++;
  }
  const v6 = retainedResponses('v6'), v6Root = gallery.captureConfig('v6').root, v7Root = gallery.captureConfig('v7').root;
  responses = new Map([...v6].map(([url, bytes]) => [url.replace(v6Root, v7Root), bytes]));
  requests.length = 0;
  await select('v7'); assertPending('v7');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v7Root)));
  assert.equal(objectURLs.size, 0);
  responses = v6; requests.length = 0;
  await elements.reload.handlers.click(); await settled(); assertPending('v7');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v7Root)));
  console.log(JSON.stringify({result:'PASS',missingV7:true,mismatchedCaptureRejected:true,corruptedPNGRejected:true,corruptedRecordRejected:true,noFallback:true,retainedVersions:versions,selections,browserEvidence:false,nativeRun:false}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
