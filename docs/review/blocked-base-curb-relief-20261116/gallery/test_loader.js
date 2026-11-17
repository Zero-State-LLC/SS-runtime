'use strict';
// Synthetic DOM/network harness only. This is not browser or native-run evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const nodeCrypto = require('node:crypto');
const gallery = require('./gallery.js');
const {packet,sha,clone,syntheticV9} = require('./test_helpers.js');

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
assert.equal(gallery.DEFAULT_CAPTURE, 'v9');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
assert.match(html, /<option value="v9" selected>/);
assert.doesNotMatch(html, /<option value="v8" selected>/);
assert.match(html, /benchmark NOT MET/);
Object.assign(elements.capture, { value: gallery.DEFAULT_CAPTURE });
const options = Object.fromEntries(['v7', 'v8', 'v9'].map(id => [id, new Element()]));
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
  // Retained V8 exists, but absent default V9 must not silently select it.
  responses = retainedResponses('v8');
  gallery.initGallery();
  await settled();
  assertPending('v9');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(gallery.captureConfig('v9').root)));
  assert.equal(objectURLs.size, 0);
  let selections = 0, versions = 0, missingDependencyCases = 0;
  const ids = ['v7', 'v8'];
  if (fs.existsSync(path.resolve(__dirname, gallery.captureConfig('v9').root, 'verification.json'))) ids.push('v9');
  else assert.ok(!process.argv.includes('--require-v9'), 'Actual V9 evidence required');
  const actualVersions = ids.length;
  for (const entry of [...ids.map(id => ({id,map:retainedResponses(id)})),{id:'v9',map:syntheticV9().map,synthetic:true}]) {
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
        if (id === 'v8' || id === 'v9') {
          const captions = descendants(elements.captures).filter(node => /logical CSS px/.test(node.textContent));
          assert.equal(captions.length,images.length);
          const baselineLabel = id === 'v9' ? 'baselineV8' : 'baselineV7';
          const candidateLabel = id === 'v9' ? 'candidateV9' : 'candidateV8';
          assert.ok(captions.every(c => c.textContent.startsWith(baselineLabel + ' ·') || c.textContent.startsWith(candidateLabel + ' ·')));
          if (arm !== 'paired') assert.ok(captions.every(c => c.textContent.startsWith(arm === 'baseline' ? baselineLabel : candidateLabel)));
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
      missingDependencyCases++;
      if(missingDependencyCases%50===0) console.log('JCODE_PROGRESS '+JSON.stringify({current:missingDependencyCases,unit:'dependency deletions',message:'Every removed evidence dependency fails closed'}));
    }
    const ordinaryAssembly = JSON.parse(valid.get(gallery.captureConfig(id).assembly));
    const sourceURL = '../../../../' + ordinaryAssembly.sources[0].image.path;
    responses = new Map(valid); responses.set(sourceURL,Buffer.from('SYNTHETIC corrupted source'));
    await select(id); assertPending(id); assert.match(elements.error.textContent,/Source bytes differ/);
    const forged = clone(JSON.parse(valid.get(root + 'verification.json')));
    forged.testExecutable.expectedBuildSHA256 = '0'.repeat(64);
    responses = new Map(valid); responses.set(root + 'verification.json',Buffer.from(JSON.stringify(forged)));
    await select(id); assertPending(id); assert.match(elements.error.textContent,/executable binding/);
    const forgedRecord = clone(record), forgedVerification = clone(JSON.parse(valid.get(root + 'verification.json')));
    // Historical metadata edits must fail their independent byte pin.
    if (id === 'v7' || id === 'v8') forgedRecord.forgedMetadata = true;
    else {
      forgedRecord.loadedTestExecutable.sha256 = packet('v8').record.loadedTestExecutable.sha256;
      forgedVerification.testExecutable.loadedSHA256 = forgedVerification.testExecutable.expectedBuildSHA256 = forgedRecord.loadedTestExecutable.sha256;
    }
    const forgedBytes = Buffer.from(JSON.stringify(forgedRecord));
    forgedVerification.files['source-scene-records.json'] = sha(forgedBytes);
    responses = new Map(valid);
    responses.set(root + 'source-scene-records.json',forgedBytes);
    responses.set(root + 'verification.json',Buffer.from(JSON.stringify(forgedVerification)));
    await select(id); assertPending(id);
    assert.match(elements.error.textContent,id === 'v9' ? /Stale V8 executable/ : /Immutable V[78] records differ/);
    if (id === 'v9') {
      const config=gallery.captureConfig(id), assembly=JSON.parse(valid.get(config.assembly));
      const manifest=JSON.parse(valid.get('../../../../'+assembly.supplementalBinding.manifest.path));
      const requiredPaths=[assembly.supplementalBinding.manifest.path,
        gallery.FINAL_SOURCE+'geometry.json',manifest.sprites[0].image.path,
        assembly.supplementalBinding.recommendation.evidence.path,
        gallery.SOURCE_ROOT+'attempt-01/registration.json'];
      for(const path of requiredPaths){
        responses=new Map(valid);responses.set('../../../../'+path,Buffer.from('corrupted dependency bytes'));
        await select(id);assertPending(id);assert.equal(objectURLs.size,0);
        assert.match(elements.error.textContent,/Supplemental bytes differ/);
      }
      // Rehash the outer containers so rejection comes from the exact native
      // binding contract, not merely from a stale record/assembly hash.
      const mutations=[
        a=>delete a.supplementalBinding,
        a=>a.supplementalBinding.dependencies.pop(),
        a=>a.supplementalBinding.manifest.path=gallery.SOURCE_ROOT+'manifest.json',
        a=>a.supplementalBinding.recommendation.decision='pending',
        a=>a.supplementalBinding.recommendation.evidence.path=gallery.FINAL_SOURCE+'README.md',
        a=>a.supplements[0].sha256='0'.repeat(64),
        a=>a.supplementalBinding.dependencies[0].path='docs/review/../escape'
      ];
      for(const mutate of mutations){
        const aa=clone(assembly),rr=clone(record),vv=clone(JSON.parse(valid.get(root+'verification.json')));
        mutate(aa);const ab=Buffer.from(JSON.stringify(aa));rr.assemblySHA256=sha(ab);
        const rb=Buffer.from(JSON.stringify(rr));vv.files['source-scene-records.json']=sha(rb);
        responses=new Map(valid);responses.set(config.assembly,ab);responses.set(root+'source-scene-records.json',rb);responses.set(root+'verification.json',Buffer.from(JSON.stringify(vv)));
        await select(id);assertPending(id);assert.equal(objectURLs.size,0);
      }
    }
    versions++;
  }
  const v8 = retainedResponses('v8'), v8Root = gallery.captureConfig('v8').root, v9Root = gallery.captureConfig('v9').root;
  responses = new Map([...v8].map(([url, bytes]) => [url.replace(v8Root, v9Root), bytes]));
  requests.length = 0;
  await select('v9'); assertPending('v9');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v9Root)));
  assert.equal(objectURLs.size, 0);
  responses = v8; requests.length = 0;
  await elements.reload.handlers.click(); await settled(); assertPending('v9');
  assert.equal(requests.length, 2);
  assert.ok(requests.every(url => url.startsWith(v9Root)));
  console.log(JSON.stringify({result:'PASS',missingV9:true,mismatchedCaptureRejected:true,corruptedPNGRejected:true,corruptedRecordRejected:true,missingDependenciesRejected:true,missingDependencyCases,sourceForgeryRejected:true,binaryForgeryRejected:true,noFallback:true,actualVersions,syntheticV9Loader:true,selections,browserEvidence:false,nativeRun:false}));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
