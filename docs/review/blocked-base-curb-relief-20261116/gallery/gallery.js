'use strict';
// ADAPT: footprint-ground-repair-20261116/gallery/gallery.js:1-281.
// Historical V7/V8 validation is retained, V9 supplements are separately bound.

const DEFAULT_CAPTURE = 'v9';
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
    root: '../../footprint-ground-repair-20261116/scene/native-capture-v8/',
    assembly: '../../footprint-ground-repair-20261116/scene/assembly.json',
    input: '../../footprint-ground-repair-20261116/scene/native-inputs-v8/native-inputs.json',
    recordHash: 'f7a8e0119307305fa4cfd15281871f1c852787d3f6c1ba3d0bc2342c421bf762',
    harness: '../../../../AppTests/FootprintGroundSceneTests.swift',
    version: 'source-scene-footprint-008-ground-plan',
    recordSchema: 'source-scene-records-008',
    arms: ['control', 'candidate'],
    pendingLabel: 'v8 shared ground/base/prop repair: pending evidence verification',
    verifiedLabel: 'v8 shared ground/base/prop repair: hash-verified, not acceptance',
    label: 'baselineV7 against candidateV8 shared ground/base/prop repair; not owner acceptance'
  }),
  'v9': Object.freeze({
    root: '../scene/native-capture-v9/',
    assembly: '../scene/assembly.json',
    input: '../scene/native-inputs-v9/native-inputs.json',
    harness: '../../../../AppTests/BlockedBaseCurbSceneTests.swift',
    version: 'source-scene-base-curb-009-relief',
    recordSchema: 'source-scene-records-009',
    arms: ['control', 'candidate'],
    pendingLabel: 'v9 blocked base and curb relief: pending evidence verification',
    verifiedLabel: 'v9 blocked base and curb relief: hash-verified, not acceptance',
    label: 'baselineV8 versus candidateV9 supplementary relief; not owner acceptance'
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
const SOURCE_ROOT = 'docs/review/blocked-base-curb-relief-20261116/source/';
const FINAL_SOURCE = SOURCE_ROOT + 'attempt-02/';
const FINAL_MANIFEST_SHA256 = '5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891';
const V8_DIRECTORY = 'docs/review/footprint-ground-repair-20261116/';
const ORDINARY_ROLES = ['paving','camera','player','stone','kiosk','context-01','context-02','context-04','context-05','ground-plan'];

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
  if (captureID === 'v9') {
    need(record.baselineRecordSHA256 === CAPTURES.v8.recordHash, 'Wrong immutable V8 baseline');
    need(SHA256.test(record.planSHA256), 'Missing unchanged V8 plan hash');
    need(equal(Object.keys(record.sourceSHA256 || {}).sort(), [...ORDINARY_ROLES].sort()) && Object.values(record.sourceSHA256).every(value => SHA256.test(value)), 'Wrong V9 ordinary source census');
    need(!Object.hasOwn(record, 'supplementalSource') && record.supplementalManifestSHA256 === FINAL_MANIFEST_SHA256, 'Missing/stale exact final supplemental manifest hash');
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
    if (captureID === 'v9') {
      need(capture.comparisonRole === (arm === 'control' ? 'BASELINE_V8_CANDIDATE' : 'CANDIDATE_V9_BASE_CURB_RELIEF'), 'Wrong V9 comparison meaning');
      need(capture.solidCount === 24, 'Authoritative solid census changed');
      const count = arm === 'candidate' ? 53 : 0;
      need(capture.uprightCount === 18 && capture.supplementalCount === count && capture.totalPresentationUprightCount === 18 + count, 'Wrong separate ordinary/supplemental census');
      need(Array.isArray(capture.supplementalActors) && capture.supplementalActors.length === count && Array.isArray(capture.supplementalSourceWitnesses) && capture.supplementalSourceWitnesses.length === count, 'Missing supplemental native witnesses');
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
    safePath(image.path);
    need(image.path.startsWith('docs/review/'), 'Unsafe source path');
    need(SHA256.test(image.sha256) && image.sha256 === record.sourceSHA256[source.role], 'Captured source hash differs: ' + source.role);
    return image;
  });
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]));
  return value;
}
function equal(a, b) { return JSON.stringify(canonical(a)) === JSON.stringify(canonical(b)); }
function keys(value, expected, label) {
  need(value && !Array.isArray(value) && equal(Object.keys(value).sort(), [...expected].sort()), 'Wrong exact ' + label + ' fields');
}
function safePath(path) {
  need(typeof path === 'string' && /^[a-zA-Z0-9_./-]+$/.test(path) && !path.startsWith('/') && path.split('/').every(p => p !== '' && p !== '.' && p !== '..'), 'Unsafe supplemental dependency path');
  return path;
}
function dependency(file) {
  keys(file, ['path','sha256'], 'dependency'); safePath(file.path);
  need(typeof file.sha256 === 'string' && SHA256.test(file.sha256), 'Invalid supplemental dependency hash');
  return file;
}
function validateSupplements(record, assembly) {
  need(record.supplementalManifestSHA256 === FINAL_MANIFEST_SHA256 && !Object.hasOwn(record, 'supplementalSource'), 'Missing/stale final supplemental manifest hash');
  need(assembly?.schema === 'blocked-base-curb-assembly-009' && assembly.fixtureVersion === CAPTURES.v9.version && assembly.baselineRecordSHA256 === CAPTURES.v8.recordHash, 'Wrong V9 assembly envelope');
  const binding = assembly.supplementalBinding;
  keys(binding, ['schema','manifest','dependencies','recommendation'], 'supplemental binding');
  need(binding.schema === 'blocked-base-curb-recommendations-009', 'Unknown supplemental recommendation schema');
  dependency(binding.manifest);
  need(binding.manifest.path === FINAL_SOURCE + 'manifest.json' && binding.manifest.sha256 === FINAL_MANIFEST_SHA256, 'Only pinned final attempt02 manifest allowed');
  const rec = binding.recommendation;
  keys(rec, ['reviewerRole','decision','scope','manifestSHA256','evidence'], 'coordinator recommendation');
  need(rec.reviewerRole === 'coordinator' && rec.decision === 'recommended' && rec.scope === 'isolated-ordinary-scene' && rec.manifestSHA256 === FINAL_MANIFEST_SHA256, 'Missing/stale coordinator supplemental recommendation');
  dependency(rec.evidence);
  need(!rec.evidence.path.startsWith(SOURCE_ROOT) && rec.evidence.path !== SOURCE_ROOT.slice(0,-1), 'Source cannot supply coordinator evidence');
  need(Array.isArray(binding.dependencies) && binding.dependencies.length > 0, 'Missing complete supplemental dependencies');
  binding.dependencies.forEach(dependency);
  need(new Set(binding.dependencies.map(d => d.path)).size === binding.dependencies.length, 'Duplicate supplemental dependencies');
  need(Array.isArray(assembly.supplements) && assembly.supplements.length === 53, 'Wrong normalized supplemental census');
  return binding;
}

// ADAPT scene/supplement_binding.py:136-208. The pinned final manifest is source
// authority. This browser checks its full byte closure, not a synthetic protocol.
function supplementalDependencies(record, assembly, manifest) {
  const binding = validateSupplements(record, assembly);
  need(manifest.schema === 'blocked-base-curb-source-009' && manifest.attempt === 2 && manifest.maximumAttempts === 2 && manifest.status === 'FINAL_CORRECTION_PENDING_COORDINATOR' && manifest.sourceRecommendation === null && manifest.nativeEvidence === false, 'Wrong final supplemental manifest');
  need(manifest.files && typeof manifest.files === 'object' && !Array.isArray(manifest.files), 'Missing final source files');
  const required = ['geometry.json','materials.json','replay.py','author.py','test_source.py','attempt-01-frozen-sha256.json','output/registration.json','ADAPT.md'];
  need(required.every(name => Object.hasOwn(manifest.files, name)), 'Incomplete editable final source dependencies');
  const files = Object.keys(manifest.files).sort().map(name => dependency({path: FINAL_SOURCE + safePath(name), sha256:manifest.files[name]}));
  need(equal(binding.dependencies, files), 'Exact complete supplemental dependency list differs');
  const merged = new Map();
  function add(file) { dependency(file); need(!merged.has(file.path) || merged.get(file.path).sha256 === file.sha256, 'Conflicting dependency hash'); merged.set(file.path,file); }
  [binding.manifest,binding.recommendation.evidence,...files].forEach(add);
  for (const name of ['baselineFiles','firstAttemptFiles']) {
    const map = manifest[name];
    need(map && typeof map === 'object' && !Array.isArray(map) && Object.keys(map).length > 0, 'Missing frozen ' + name);
    Object.entries(map).forEach(([path,sha256]) => add({path,sha256}));
  }
  need(manifest.baselineFiles[V8_DIRECTORY + 'scene/native-capture-v8/source-scene-records.json'] === CAPTURES.v8.recordHash, 'Frozen V8 baseline linkage missing');
  need(Array.isArray(manifest.sprites) && manifest.sprites.length === 53, 'Final source sprite census');
  for (const sprite of manifest.sprites) {
    dependency(sprite.image);
    need(sprite.image.path === FINAL_SOURCE + 'output/sprites/' + sprite.id + '.png' && manifest.files['output/sprites/' + sprite.id + '.png'] === sprite.image.sha256, 'Supplemental PNG outside final manifest');
    add(sprite.image);
  }
  return [...merged.values()];
}

function validateSupplementPayload(record, assembly, manifest, documents, input) {
  supplementalDependencies(record, assembly, manifest);
  const doc = path => { need(documents.has(path), 'Missing supplemental JSON dependency: ' + path); return documents.get(path); };
  const baseline = doc(V8_DIRECTORY + 'scene/native-capture-v8/source-scene-records.json');
  const oldAssembly = doc(V8_DIRECTORY + 'scene/assembly.json');
  keys(record, [...Object.keys(baseline),'supplementalManifestSHA256'], 'native V9 record');
  keys(assembly, [...Object.keys(oldAssembly),'supplementalBinding','supplements'], 'native V9 assembly');
  for (const key of Object.keys(oldAssembly).filter(k => !['schema','fixtureVersion','baselineRecordSHA256'].includes(k))) need(equal(assembly[key], oldAssembly[key]), 'Immutable V8 assembly changed: ' + key);
  validateBaseline(record, baseline);
  need(equal(record.sourceSHA256, baseline.sourceSHA256), 'V9 ordinary source census changed');
  need(manifest.baselineFiles[V8_DIRECTORY + 'scene/assembly.json'] === baseline.assemblySHA256 && manifest.baselineFiles[V8_DIRECTORY + 'scene/native-inputs-v8/native-inputs.json'] === baseline.inputSHA256, 'Immutable V8 assembly/input linkage differs');
  const geometry = doc(FINAL_SOURCE + 'geometry.json');
  need(equal(geometry, doc(SOURCE_ROOT + 'geometry.json')) && geometry.schema === 'blocked-base-curb-geometry-009' && geometry.presentationOnly === true, 'Frozen final geometry changed');
  need(equal(manifest.sprites, doc(FINAL_SOURCE + 'output/registration.json')), 'Final registration differs');
  need(equal(manifest.firstAttemptFiles, doc(FINAL_SOURCE + 'attempt-01-frozen-sha256.json')), 'First attempt freeze differs');
  const oldHashes = doc(SOURCE_ROOT + 'baseline-sha256.json');
  need(Object.entries(oldHashes).every(([path,digest]) => manifest.baselineFiles[path] === digest), 'Immutable V8 dependencies missing');
  const oldSprites = doc(SOURCE_ROOT + 'attempt-01/registration.json');
  need(oldSprites.length === 53 && geometry.sprites.length === 53, 'Geometry/first source census differs');
  const normalized = manifest.sprites.map((sprite,index) => {
    const prior = oldSprites[index];
    const withoutImage = value => Object.fromEntries(Object.entries(value).filter(([key]) => key !== 'image'));
    need(equal(withoutImage(sprite), withoutImage(prior)) && sprite.geometryID === geometry.sprites[index].id, 'Final source geometry/registration changed');
    return {role:sprite.id,nodeName:'supplement-'+sprite.id,file:sprite.id+'.png',sha256:sprite.image.sha256,registration:sprite.registration,
      verticesWorldXYZ:sprite.geometryLandmarks.map(v => v.worldXYZ),verticesPixelsTopLeft:sprite.geometryLandmarks.map(v => v.sourcePixelsTopLeft),footprintWorld:[...sprite.worldBoundsXYZ.min.slice(0,2),...sprite.worldBoundsXYZ.max.slice(0,2)]};
  });
  need(equal(assembly.supplements, normalized), 'Normalized supplemental geometry/image bindings differ');
  const oldInput = doc(V8_DIRECTORY + 'scene/native-inputs-v8/native-inputs.json');
  keys(input, [...Object.keys(oldInput),'supplements','supplementalBinding','supplementalManifestSHA256'], 'prepared V9 input');
  need(input.schema === 'source-scene-native-009' && input.fixtureVersion === CAPTURES.v9.version && input.assemblySHA256 === record.assemblySHA256 && input.harnessSourceSHA256 === record.harnessSourceReadSHA256 && input.baselineRecordSHA256 === CAPTURES.v8.recordHash && input.supplementalManifestSHA256 === FINAL_MANIFEST_SHA256, 'Prepared supplemental source linkage differs');
  need(equal(input.supplements,normalized) && equal(input.supplementalBinding,assembly.supplementalBinding), 'Prepared supplemental binding differs');
  for (const key of Object.keys(oldInput).filter(k => !['schema','fixtureVersion','assemblySHA256','harnessSourceSHA256','baselineRecordSHA256'].includes(k))) need(equal(input[key],oldInput[key]), 'Unchanged V8 prepared source changed: ' + key);
  for (const capture of record.captures) {
    const expected = capture.arm === 'candidate' ? normalized : [];
    need(equal(capture.supplementalActors.map(a => a.name),expected.map(s => s.nodeName)), 'Native supplemental actor census differs');
    need(capture.supplementalSourceWitnesses.length === expected.length, 'Native supplemental witness census differs');
    capture.supplementalSourceWitnesses.forEach((w,i) => {
      const s=expected[i];
      keys(w,['nodeName','role','sourceSHA256','footprintWorld','vertices'],'native supplemental witness');
      need(w.nodeName===s.nodeName && w.role===s.role && w.sourceSHA256===s.sha256 && equal(w.footprintWorld,s.footprintWorld), 'Native supplemental source/geometry witness differs');
      need(equal(w.vertices.map(v=>v.worldXYZ),s.verticesWorldXYZ) && equal(w.vertices.map(v=>v.sourcePixelsTopLeft),s.verticesPixelsTopLeft), 'Native supplemental XYZ/source vertices differ');
    });
  }
  return normalized;
}

async function verifySupplementalEvidence(record, assembly, input, fetchBytes = bytesAt) {
  const binding=validateSupplements(record,assembly), cache=new Map(), documents=new Map();
  async function read(file) {
    dependency(file);
    if (!cache.has(file.path)) cache.set(file.path, fetchBytes('../../../../'+file.path).then(async bytes => {
      need(await hash(bytes) === file.sha256, 'Supplemental bytes differ: '+file.path);
      if (file.path.endsWith('.json')) documents.set(file.path,JSON.parse(new TextDecoder().decode(bytes)));
      return bytes;
    }));
    return cache.get(file.path);
  }
  await read(binding.manifest);
  const manifest=documents.get(binding.manifest.path);
  const dependencies=supplementalDependencies(record,assembly,manifest);
  // Rehash every declared final, baseline and frozen-first dependency each load.
  for (let start=0; start<dependencies.length; start+=8) await Promise.all(dependencies.slice(start,start+8).map(read));
  return validateSupplementPayload(record,assembly,manifest,documents,input);
}

function validateBaseline(record, baseline) {
  for (const [role,digest] of Object.entries(baseline.sourceSHA256)) {
    need(record.sourceSHA256[role] === digest, 'Frozen V7 source differs: ' + role);
  }
  if (record.fixtureVersion === CAPTURES.v9.version) {
    need(record.planSHA256 === baseline.planSHA256, 'V8 ground plan changed');
    need(record.loadedTestExecutable.sha256 !== baseline.loadedTestExecutable.sha256, 'Stale V8 executable cannot establish V9');
  } else {
    need(record.loadedTestExecutable.sha256 !== baseline.loadedTestExecutable.sha256, 'Stale V7 executable cannot establish V8');
  }
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
      const armLabel = state.captureID === 'v9' ? (capture.arm === 'control' ? 'baselineV8' : 'candidateV9') : state.captureID === 'v8' ? (capture.arm === 'control' ? 'baselineV7' : 'candidateV8') : capture.comparisonRole === 'BASELINE_V6_CANDIDATE' ? 'V7 historical control (v6 appearance)' : 'V7 immutable candidate (owner rejected)';
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
      if (config.recordHash) need(recordDigest === config.recordHash, `Immutable ${captureID.toUpperCase()} records differ`);
      const inputBytes = await bytesAt(config.input);
      need(await hash(inputBytes) === record.inputSHA256, 'Prepared input bytes differ');
      need(await hash(await bytesAt(config.harness)) === record.harnessSourceReadSHA256, 'Harness source bytes differ');
      if (captureID === 'v8' || captureID === 'v9') {
        const parent = captureID === 'v9' ? CAPTURES.v8 : CAPTURES.v7;
        const baselineBytes = await bytesAt(parent.root + 'source-scene-records.json');
        need(await hash(baselineBytes) === parent.recordHash, 'Immutable baseline bytes differ');
        validateBaseline(record, JSON.parse(new TextDecoder().decode(baselineBytes)));
        need(await hash(await bytesAt('../../footprint-ground-repair-20261116/plan/plan.json')) === record.planSHA256, 'Shared plan bytes differ');
      }
      const assemblyBytes = await bytesAt(config.assembly);
      need(await hash(assemblyBytes) === record.assemblySHA256, 'Assembly bytes differ from captured source');
      const assembly = JSON.parse(new TextDecoder().decode(assemblyBytes));
      const sources = validateSources(record, assembly);
      for (const source of sources) {
        need(await hash(await bytesAt('../../../../' + source.path)) === source.sha256, 'Source bytes differ: ' + source.path);
      }
      if (captureID === 'v9') await verifySupplementalEvidence(record, assembly, JSON.parse(new TextDecoder().decode(inputBytes)));
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

if (typeof module !== 'undefined' && module.exports) module.exports = { validateSupplements, supplementalDependencies, validateSupplementPayload, verifySupplementalEvidence, validateBaseline, validateSources, validateEvidence, selectedImage, captureConfig, initGallery, CAPTURES, DEFAULT_CAPTURE, STATUS, FINAL_SOURCE, FINAL_MANIFEST_SHA256, SOURCE_ROOT, V8_DIRECTORY };
if (typeof document !== 'undefined') initGallery();
