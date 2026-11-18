'use strict';

const DEFAULT_CAPTURE = 'v8';
const CAPTURES = Object.freeze({
  'v7': Object.freeze({
    root: '../../building-perspective-detail-20261116/scene/native-capture-v7/',
    assembly: '../../building-perspective-detail-20261116/scene/assembly.json',
    input: '../../building-perspective-detail-20261116/scene/native-inputs-v7/native-inputs.json',
    harness: '../../../../AppTests/BuildingPerspectiveSceneTests.swift',
    recordHash: '9728f0a030020dff0caad52e8d3791be092a3b6ada8b5ffd845ee9d370785889',
    version: 'source-scene-building-007-perspective-detail',
    recordSchema: 'source-scene-records-007',
    arms: ['control', 'candidate'],
    pendingLabel: 'v7 building perspective/detail: pending evidence verification',
    verifiedLabel: 'v7 building perspective/detail: hash-verified capture, not acceptance',
    label: 'building-only comparison against v6-style baseline; owner acceptance not granted'
  }),
  'v8': Object.freeze({
    root: '../scene/native-capture-v8/',
    assembly: '../scene/assembly.json',
    input: '../scene/native-inputs-v8/native-inputs.json',
    harness: '../../../../AppTests/FootprintGroundSceneTests.swift',
    version: 'source-scene-footprint-008-ground-plan',
    recordSchema: 'source-scene-records-008',
    arms: ['control', 'candidate'],
    pendingLabel: 'v8 shared ground/base/prop repair: pending evidence verification',
    verifiedLabel: 'v8 shared ground/base/prop repair: hash-verified, not acceptance',
    label: 'baselineV7 against candidateV8 shared ground/base/prop repair; not owner acceptance'
  })
});
function captureConfig(id) {
  need(Object.hasOwn(CAPTURES, id), 'Unsupported capture selection');
  return CAPTURES[id];
}
const STATUS = 'NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE';
const ZOOMS = [1, 1.25, 1.4];
const ARMS = ['control', 'candidate'];
const SUFFIXES = ['-native', '-half', '-grayscale'];
const SHA256 = /^[0-9a-f]{64}$/;

function need(condition, message) {
  if (!condition) throw new Error(message);
}

function validateEvidence(record, verification, captureID = DEFAULT_CAPTURE) {
  const config = captureConfig(captureID);
  need(!Object.hasOwn(record, 'syntheticFixture') && !Object.hasOwn(verification, 'syntheticFixture'), 'Synthetic is not native evidence');
  need(verification.status === STATUS && record.status === STATUS, 'Wrong verification/record status');
  need(verification.fixtureVersion === config.version && record.fixtureVersion === config.version, 'Wrong fixture version');
  if (config.recordSchema) need(record.schema === config.recordSchema, 'Wrong records schema for selected capture');
  need(verification.nativeTests === 1 && verification.captures === 6 && verification.images === 18, 'Expected one native test, six captures, eighteen images');
  for (const key of ['ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence']) {
    need(verification[key] === false, 'Unsupported acceptance scope: ' + key);
    need(!Object.hasOwn(record,key) || record[key] === false, 'Unsupported record acceptance scope: ' + key);
  }
  need(record.fixture === 'south-neutral-camera-neutral' && record.cameraSourceFrames === 1 && record.playerSourceFrames === 1, 'Not the static quiet source fixture');
  need(SHA256.test(record.inputSHA256) && record.inputSHA256 === verification.inputSHA256, 'Input binding differs');
  need(SHA256.test(record.harnessSourceReadSHA256) && record.harnessSourceReadSHA256 === verification.harnessSourceReadSHA256, 'Harness binding differs');
  const executable = verification.testExecutable || {};
  need(SHA256.test(executable.loadedSHA256) && executable.loadedSHA256 === executable.expectedBuildSHA256 && executable.loadedSHA256 === record.loadedTestExecutable?.sha256, 'Loaded executable binding differs');
  need(Array.isArray(record.captures) && record.captures.length === 6, 'Six capture records required');
  need(SHA256.test(verification.files?.['source-scene-records.json']), 'Missing records file hash');
  const expected = (config.arms || ARMS).flatMap(arm => ZOOMS.map(zoom => [arm, zoom]));
  if (captureID === 'v8') {
    need(record.baselineRecordSHA256 === CAPTURES.v7.recordHash, 'Wrong immutable V7 baseline');
    need(SHA256.test(record.planSHA256), 'Missing shared plan hash');
    need(JSON.stringify(Object.keys(record.sourceSHA256 || {}).sort()) === JSON.stringify(['paving','camera','player','stone','kiosk','context-01','context-02','context-04','context-05','ground-plan'].sort()), 'Wrong V8 source census');
    need(Object.values(record.sourceSHA256).every(value => SHA256.test(value)), 'Invalid V8 source hash');
  }
  if (captureID === 'v7') {
    need(record.baselineRecordSHA256 === '1cc28f757fb6e9e7ed6e53843c745bcb63f8adc42a2eef6413362582eac4930d', 'Wrong immutable v6 baseline');
    need(JSON.stringify(Object.keys(record.sourceSHA256 || {}).sort()) === JSON.stringify(['paving','camera','player','stone','kiosk','context-01','context-02','context-04','context-05'].sort()), 'Wrong building source census');
    need(Object.values(record.sourceSHA256).every(value => SHA256.test(value)), 'Invalid building source hash');
  }
  const files = [];
  record.captures.forEach((capture, index) => {
    const [arm, zoom] = expected[index];
    need(capture.arm === arm && capture.zoom === zoom, 'Missing, duplicate or reordered capture');
    if (captureID === 'v7') {
      need(capture.comparisonRole === (arm === 'control' ? 'BASELINE_V6_CANDIDATE' : 'CANDIDATE_V7_BUILDING_ONLY'), 'Wrong building comparison meaning');
      need(capture.solidCount === 24, 'Authoritative solid census changed');
    }
    if (captureID === 'v8') {
      need(capture.comparisonRole === (arm === 'control' ? 'BASELINE_V7_CANDIDATE' : 'CANDIDATE_V8_SHARED_GROUND_PLAN'), 'Wrong V8 comparison meaning');
      need(capture.solidCount === 24, 'Authoritative solid census changed');
    }
    need(capture.name === `source-scene-${arm}-ordinary-z${Math.round(zoom * 100)}` && capture.mode === 'ordinary', 'Unsafe or unexpected capture identity');
    for (const flag of ['hudVisible', 'controlsRetained', 'fieldVisible', 'fieldUnchanged']) {
      need(capture[flag] === true, 'Missing ordinary presentation evidence: ' + flag);
    }
    need(capture.authorityBefore && capture.authorityBefore === capture.authorityAfter && capture.solidCount > 0 && capture.cameraRange > 0, 'Authority/solid evidence missing');
    const pixels = capture.nativePixels;
    need(Array.isArray(pixels) && pixels.length === 2 && Number.isInteger(pixels[0]) && Number.isInteger(pixels[1]), 'Native dimensions missing');
    const density = pixels[0] / 704;
    need(Number.isInteger(density) && density >= 1 && density <= 4 && pixels[1] === 326 * density, 'Invalid native pixel density/crop');
    need(JSON.stringify(Object.keys(capture.pngSHA256 || {}).sort()) === JSON.stringify([...SUFFIXES].sort()), 'Wrong PNG suffix census');
    for (const suffix of SUFFIXES) {
      const name = capture.name + suffix + '.png';
      const digest = capture.pngSHA256[suffix];
      need(SHA256.test(digest) && verification.files[name] === digest, 'Capture/verification image hash differs: ' + name);
      files.push({ name, digest, pixels: suffix === '-half' ? pixels.map(value => value / 2) : [...pixels] });
    }
  });
  need(Object.keys(verification.files).filter(name => name.endsWith('.png')).length === 18, 'Verification PNG census differs');
  return files;
}

function selectedImage(capture, size, grayscale) {
  need(size === 'native' || size === 'half', 'Unsupported display size');
  const suffix = grayscale ? '-grayscale' : size === 'half' ? '-half' : '-native';
  return { name: capture.name + suffix + '.png', width: size === 'half' ? 352 : 704, height: size === 'half' ? 163 : 326 };
}

function validateSources(record, assembly) {
  need(assembly.fixtureVersion === record.fixtureVersion, 'Assembly fixture differs');
  need(Array.isArray(assembly.sources), 'Missing source inventory');
  const roles = assembly.sources.map(source => source.role);
  need(new Set(roles).size === roles.length && JSON.stringify([...roles].sort()) === JSON.stringify(Object.keys(record.sourceSHA256).sort()), 'Source role census differs');
  return assembly.sources.map(source => {
    const image = source.image || {};
    need(typeof image.path === 'string' && /^docs\/review\/[a-zA-Z0-9_./-]+$/.test(image.path) && !image.path.split('/').includes('..'), 'Unsafe source path');
    need(SHA256.test(image.sha256) && image.sha256 === record.sourceSHA256[source.role], 'Captured source hash differs: ' + source.role);
    return image;
  });
}

function validateBaseline(record, baseline) {
  for (const [role,digest] of Object.entries(baseline.sourceSHA256)) {
    need(record.sourceSHA256[role] === digest, 'Frozen V7 source differs: ' + role);
  }
  need(record.loadedTestExecutable.sha256 !== baseline.loadedTestExecutable.sha256, 'Stale V7 executable cannot establish V8');
}

async function bytesAt(url) {
  const response = await fetch(url, { cache: 'no-store' });
  need(response.ok, `Missing evidence: ${url} (HTTP ${response.status})`);
  return response.arrayBuffer();
}

async function hash(bytes) {
  need(globalThis.crypto?.subtle, 'SHA256 verification requires localhost or HTTPS');
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(value => value.toString(16).padStart(2, '0')).join('');
}

function loadImage(url) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    const timer = setTimeout(() => reject(new Error('Timed out loading evidence image')), 15000);
    image.onload = () => { clearTimeout(timer); resolve(image); };
    image.onerror = () => { clearTimeout(timer); reject(new Error('Invalid or missing evidence PNG')); };
    image.src = url;
  });
}

function initGallery() {
  const element = id => document.getElementById(id);
  let state = null;
  let generation = 0;
  let liveURLs = [];

  function render() {
    if (!state) return;
    const zoom = Number(element('zoom').value);
    const selectedArm = element('arm').value;
    const arm = selectedArm === 'baseline' ? captureConfig(state.captureID).arms[0] : selectedArm === 'candidate' ? captureConfig(state.captureID).arms[1] : selectedArm;
    const size = element('size').value;
    const grayscale = element('grayscale').checked;
    const rows = state.record.captures.filter(capture => capture.zoom === zoom && (arm === 'paired' || capture.arm === arm));
    need(rows.length === (arm === 'paired' ? 2 : 1), 'Selected capture is unavailable');
    const fragment = document.createDocumentFragment();
    for (const capture of rows) {
      const selected = selectedImage(capture, size, grayscale);
      const figure = document.createElement('figure');
      figure.className = 'capture';
      const viewport = document.createElement('div');
      viewport.className = 'viewport';
      const image = document.createElement('img');
      image.className = 'capture-image';
      image.width = selected.width;
      image.height = selected.height;
      image.alt = `${capture.arm}, zoom ${capture.zoom}, ${size}${grayscale ? ', grayscale' : ''}, quiet source comparison`;
      image.src = state.images.get(selected.name);
      image.dataset.evidenceFile = selected.name;
      const caption = document.createElement('figcaption');
      const armLabel = state.captureID === 'v8' ? (capture.arm === 'control' ? 'baselineV7' : 'candidateV8') : capture.comparisonRole === 'BASELINE_V6_CANDIDATE' ? 'V7 historical control (v6 appearance)' : 'V7 immutable candidate (owner rejected)';
      caption.textContent = `${armLabel} · zoom ${capture.zoom} · ${selected.width}×${selected.height} logical CSS px · ${selected.name}`;
      viewport.append(image);
      figure.append(viewport, caption);
      fragment.append(figure);
    }
    element('captures').dataset.size = size;
    element('captures').replaceChildren(fragment);
    element('benchmark').classList.toggle('grayscale', grayscale);
  }

  async function boot() {
    const ticket = ++generation;
    const captureID = element('capture').value;
    state = null;
    element('controls').disabled = true;
    element('reload').disabled = true;
    element('captures').replaceChildren();
    element('error').hidden = true;
    element('capture-label').textContent = '';
    element('evidence-links').hidden = true;
    element('status').textContent = `Capture ${captureID}: pending verification of records and all eighteen PNG hashes...`;
    liveURLs.forEach(url => URL.revokeObjectURL(url));
    liveURLs = [];
    const created = [];
    try {
      const config = captureConfig(captureID);
      const selectedOption = element('capture').selectedOptions?.[0];
      if (config.pendingLabel && selectedOption) selectedOption.textContent = config.pendingLabel;
      const [recordBytes, verificationBytes] = await Promise.all([bytesAt(config.root + 'source-scene-records.json'), bytesAt(config.root + 'verification.json')]);
      const record = JSON.parse(new TextDecoder().decode(recordBytes));
      const verification = JSON.parse(new TextDecoder().decode(verificationBytes));
      const required = validateEvidence(record, verification, captureID);
      const recordDigest = await hash(recordBytes);
      need(recordDigest === verification.files['source-scene-records.json'], 'Records bytes differ from importer hash');
      if (config.recordHash) need(recordDigest === config.recordHash, 'Immutable V7 records differ');
      need(await hash(await bytesAt(config.input)) === record.inputSHA256, 'Prepared input bytes differ');
      need(await hash(await bytesAt(config.harness)) === record.harnessSourceReadSHA256, 'Harness source bytes differ');
      if (captureID === 'v8') {
        const baselineBytes = await bytesAt(CAPTURES.v7.root + 'source-scene-records.json');
        need(await hash(baselineBytes) === CAPTURES.v7.recordHash, 'Immutable V7 baseline bytes differ');
        validateBaseline(record, JSON.parse(new TextDecoder().decode(baselineBytes)));
        need(await hash(await bytesAt('../plan/plan.json')) === record.planSHA256, 'Shared plan bytes differ');
      }
      const assemblyBytes = await bytesAt(config.assembly);
      need(await hash(assemblyBytes) === record.assemblySHA256, 'Assembly bytes differ from captured source');
      const sources = validateSources(record, JSON.parse(new TextDecoder().decode(assemblyBytes)));
      for (const source of sources) {
        need(await hash(await bytesAt('../../../../' + source.path)) === source.sha256, 'Source bytes differ: ' + source.path);
      }
      const images = new Map();
      // Sequential loading keeps failure cleanup deterministic, with no late object URLs.
      for (const file of required) {
        if (ticket !== generation) { created.forEach(url => URL.revokeObjectURL(url)); return; }
        const bytes = await bytesAt(config.root + file.name);
        need(await hash(bytes) === file.digest, 'PNG bytes differ from recorded hash: ' + file.name);
        const url = URL.createObjectURL(new Blob([bytes], { type: 'image/png' }));
        created.push(url);
        const image = await loadImage(url);
        need(image.naturalWidth === file.pixels[0] && image.naturalHeight === file.pixels[1], 'PNG dimensions differ: ' + file.name);
        images.set(file.name, url);
      }
      if (ticket !== generation) { created.forEach(url => URL.revokeObjectURL(url)); return; }
      liveURLs = created;
      state = { record, verification, images, captureID };
      render();
      element('controls').disabled = false;
      element('capture-label').textContent = `Capture ${captureID}: ${config.label}`;
      if (config.verifiedLabel && selectedOption) selectedOption.textContent = config.verifiedLabel;
      element('records-link').href = config.root + 'source-scene-records.json';
      element('verification-link').href = config.root + 'verification.json';
      element('evidence-links').hidden = false;
      element('status').textContent = 'Importer-verified evidence loaded: one native test reported, six captures, eighteen hash-matched PNGs. Review only, no source verdict or acceptance.';
    } catch (error) {
      created.forEach(url => URL.revokeObjectURL(url));
      if (ticket !== generation) return;
      state = null;
      element('captures').replaceChildren();
      element('status').textContent = `Capture ${captureID}: pending or invalid evidence. No native capture is displayed. No fallback to another capture.`;
      element('error').textContent = String(error.message || error) + ' Import the real capture packet, then reload. Serve this gallery over localhost/HTTPS, not file://.';
      element('error').hidden = false;
    } finally {
      if (ticket === generation) element('reload').disabled = false;
    }
  }

  for (const id of ['zoom', 'arm', 'size', 'grayscale']) element(id).addEventListener('change', render);
  element('reload').addEventListener('click', boot);
  element('capture').addEventListener('change', boot);
  const reference = element('benchmark');
  reference.addEventListener('error', () => { element('reference-error').hidden = false; });
  if (reference.complete && reference.naturalWidth === 0) element('reference-error').hidden = false;
  boot();
}

if (typeof module !== 'undefined' && module.exports) module.exports = { validateBaseline, validateSources, validateEvidence, selectedImage, captureConfig, initGallery, CAPTURES, DEFAULT_CAPTURE, STATUS };
if (typeof document !== 'undefined') initGallery();
