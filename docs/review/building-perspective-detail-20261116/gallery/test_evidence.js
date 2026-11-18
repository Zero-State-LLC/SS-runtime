'use strict';
// Protocol and retained-byte checks, not browser or new native evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const g = require('./gallery.js');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const clone = value => JSON.parse(JSON.stringify(value));
let actual = 0, images = 0, selections = 0, rejected = 0;
assert.equal(g.DEFAULT_CAPTURE, 'v7');
assert.throws(() => g.captureConfig('../v6'));
for (const id of ['v6', 'v7']) {
  const root = path.resolve(__dirname, g.captureConfig(id).root);
  if (!fs.existsSync(path.join(root, 'verification.json'))) {
    assert.equal(id, 'v7');
    assert.ok(!process.argv.includes('--require-v7'), 'Actual v7 evidence required, not a synthetic substitute');
    continue;
  }
  const bytes = fs.readFileSync(path.join(root, 'source-scene-records.json'));
  const r = JSON.parse(bytes), v = JSON.parse(fs.readFileSync(path.join(root, 'verification.json')));
  const files = g.validateEvidence(r, v, id);
  assert.equal(sha(bytes), v.files['source-scene-records.json']);
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
  assert.throws(() => g.validateEvidence(r,v,id === 'v6' ? 'v7' : 'v6'));
  actual++;
}
assert.throws(() => g.selectedImage({name:'unused'}, 'stretch', false));
console.log(JSON.stringify({result:'PASS',actualCaptureVersions:actual,images,selections,rejectedMutations:rejected,v7NativeEvidence:actual===2,browserEvidence:false}));
