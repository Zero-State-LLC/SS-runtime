'use strict';
// Protocol and retained-byte checks, not browser or new native evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const g = require('./gallery.js');
const {packet,syntheticV8} = require('./test_helpers.js');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const clone = value => JSON.parse(JSON.stringify(value));
let actual = 0, images = 0, selections = 0, rejected = 0;
assert.equal(g.DEFAULT_CAPTURE, 'v8');
assert.throws(() => g.captureConfig('../v6'));
for (const id of ['v7', 'v8']) {
  const root = path.resolve(__dirname, g.captureConfig(id).root);
  if (!fs.existsSync(path.join(root, 'verification.json'))) {
    assert.equal(id, 'v8');
    assert.ok(!process.argv.includes('--require-v8'), 'Actual v8 evidence required, not a synthetic substitute');
    continue;
  }
  const bytes = fs.readFileSync(path.join(root, 'source-scene-records.json'));
  const r = JSON.parse(bytes), v = JSON.parse(fs.readFileSync(path.join(root, 'verification.json')));
  const files = g.validateEvidence(r, v, id);
  assert.equal(sha(bytes), v.files['source-scene-records.json']);
  if (id === 'v7') assert.equal(sha(bytes), g.captureConfig(id).recordHash);
  const p = packet(id);
  assert.equal(sha(p.ab), r.assemblySHA256);
  assert.equal(sha(p.map.get(g.captureConfig(id).input)),r.inputSHA256);
  assert.equal(sha(p.map.get(g.captureConfig(id).harness)),r.harnessSourceReadSHA256);
  if (id === 'v8') {
    assert.equal(sha(p.map.get('../plan/plan.json')),r.planSHA256);
    g.validateBaseline(r,packet('v7').record);
  }
  for (const source of g.validateSources(r,p.assembly)) assert.equal(sha(p.map.get('../../../../' + source.path)),source.sha256);
  for (const change of [a => a.sources.pop(), a => a.sources.push(a.sources[0]), a => a.sources[0].image.sha256 = '0'.repeat(64), a => a.sources[0].image.path = 'docs/review/../../escape']) {
    const a = clone(p.assembly); change(a); assert.throws(() => g.validateSources(r,a)); rejected++;
  }
  for (const file of files) {
    const png = fs.readFileSync(path.join(root, file.name));
    assert.equal(sha(png), file.digest);
    assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    assert.deepEqual([png.readUInt32BE(16), png.readUInt32BE(20)], file.pixels);
    images++;
  }
  for (const c of r.captures) for (const size of ['native', 'half']) for (const gray of [false, true]) {
    const selected = g.selectedImage(c, size, gray);
    assert.ok(files.some(f => f.name === selected.name));
    assert.equal(selected.width, size === 'native' ? 704 : 352);
    assert.equal(selected.height, size === 'native' ? 326 : 163);
    selections++;
  }
  const mutations = [
    (r,v) => { r.schema = 'unknown'; },
    (r,v) => { r.fixtureVersion = 'wrong'; },
    (r,v) => { v.fixtureVersion = 'wrong'; },
    (r,v) => { v.status = 'ACCEPTED'; },
    (r,v) => { r.status = 'ACCEPTED'; },
    (r,v) => { v.nativeTests = 0; },
    (r,v) => { v.captures = 5; },
    (r,v) => { v.images = 17; },
    (r,v) => { v.ownerAcceptance = true; },
    (r,v) => { v.physicalDeviceEvidence = true; },
    (r,v) => { v.animationFamilyEvidence = true; },
    (r,v) => { r.ownerAcceptance = true; },
    (r,v) => { r.physicalDeviceEvidence = true; },
    (r,v) => { r.animationFamilyEvidence = true; },
    (r,v) => { r.inputSHA256 = '0'.repeat(64); },
    (r,v) => { r.harnessSourceReadSHA256 = '0'.repeat(64); },
    (r,v) => { v.testExecutable.expectedBuildSHA256 = '0'.repeat(64); },
    (r,v) => { r.loadedTestExecutable.sha256 = '0'.repeat(64); },
    (r,v) => { r.captures.pop(); },
    (r,v) => { r.captures[0].name = '../escape'; },
    (r,v) => { r.captures[0].arm = 'unknown'; },
    (r,v) => { r.captures[0].authorityAfter = 'changed'; },
    (r,v) => { r.captures[0].fieldUnchanged = false; },
    (r,v) => { r.captures[0].nativePixels = [704, 325]; },
    (r,v) => { r.captures[0].pngSHA256['-native'] = '0'.repeat(64); },
    (r,v) => { delete v.files['source-scene-records.json']; },
    (r,v) => { v.files['extra.png'] = '0'.repeat(64); }
  ];
  if (id === 'v7') mutations.push(
    (r,v) => { r.baselineRecordSHA256 = '0'.repeat(64); },
    (r,v) => { delete r.sourceSHA256['context-01']; },
    (r,v) => { r.sourceSHA256.kiosk = 'invalid'; },
    (r,v) => { r.captures[0].comparisonRole = 'ORIGINAL_CONTROL'; },
    (r,v) => { r.captures[0].solidCount = 23; }
  );
  for (const mutate of mutations) {
    const rr = clone(r), vv = clone(v); mutate(rr,vv);
    assert.throws(() => g.validateEvidence(rr,vv,id)); rejected++;
  }
  assert.throws(() => g.validateEvidence(r,v,id === 'v7' ? 'v8' : 'v7'));
  actual++;
}
assert.throws(() => g.selectedImage({name:'unused'}, 'stretch', false));
const synthetic = syntheticV8(), baseline = packet('v7').record;
assert.equal(g.validateEvidence(synthetic.record,synthetic.verification,'v8').length,18);
g.validateBaseline(synthetic.record,baseline);
for (const change of [
  r => r.schema = 'source-scene-records-007',
  r => r.baselineRecordSHA256 = '0'.repeat(64),
  r => delete r.planSHA256,
  r => delete r.sourceSHA256['ground-plan'],
  r => r.sourceSHA256['ground-plan'] = 'invalid',
  r => r.captures[0].comparisonRole = 'BASELINE_V6_CANDIDATE',
  r => r.captures[3].comparisonRole = 'CANDIDATE_V7_BUILDING_ONLY',
  r => r.captures[0].arm = 'baselineV7',
  r => r.captures[0].solidCount = 23,
  r => r.syntheticFixture = true
]) {
  const r = clone(synthetic.record); change(r);
  assert.throws(() => g.validateEvidence(r,synthetic.verification,'v8')); rejected++;
}
for (const change of [r => r.sourceSHA256.camera = '0'.repeat(64),r => r.loadedTestExecutable.sha256 = baseline.loadedTestExecutable.sha256]) {
  const r = clone(synthetic.record); change(r); assert.throws(() => g.validateBaseline(r,baseline)); rejected++;
}
const html = fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const css = fs.readFileSync(path.join(__dirname,'gallery.css'),'utf8');
assert.match(html, /value="v8" selected/);
assert.doesNotMatch(html, /value="v7" selected/);
assert.match(html, /Review only, not accepted/);
assert.match(html, /baselineV7 versus candidateV8/);
assert.match(html, /stone-painted-facade-20261116\/inputs\/benchmark.png/);
assert.match(css, /--logical-width: 704px; --logical-height: 326px/);
assert.match(css, /--logical-width: 352px; --logical-height: 163px/);
assert.match(css, /height: auto; object-fit: contain/);
console.log(JSON.stringify({result:'PASS',actualCaptureVersions:actual,images,selections,rejectedMutations:rejected,syntheticV8Contract:true,v8NativeEvidence:actual===2,browserEvidence:false}));
