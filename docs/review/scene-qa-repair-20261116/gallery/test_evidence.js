'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const gallery = require('./gallery.js');
let images = 0;
let selections = 0;
let rejected = 0;
const args = process.argv.slice(2);
assert.ok(args.every(arg => arg === '--require-v6'), 'Only --require-v6 is supported');
const actualIDs = args.includes('--require-v6') ? ['v4', 'v5', 'v6'] : ['v4', 'v5'];
for (const id of actualIDs) {
  const root = path.resolve(__dirname, gallery.captureConfig(id).root);
  const bytes = fs.readFileSync(path.join(root, 'source-scene-records.json'));
  const record = JSON.parse(bytes);
  const verification = JSON.parse(fs.readFileSync(path.join(root, 'verification.json')));
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), verification.files['source-scene-records.json']);
  const files = gallery.validateEvidence(record, verification, id);
  for (const file of files) {
    const image = fs.readFileSync(path.join(root, file.name));
    assert.equal(crypto.createHash('sha256').update(image).digest('hex'), file.digest);
    assert.deepEqual([image.readUInt32BE(16), image.readUInt32BE(20)], file.pixels);
    images++;
  }
  for (const row of record.captures) for (const size of ['native', 'half']) for (const gray of [false, true]) {
    const selected = gallery.selectedImage(row, size, gray);
    assert.ok(files.some(file => file.name === selected.name));
    assert.equal(selected.width, size === 'native' ? 704 : 352);
    assert.equal(selected.height, size === 'native' ? 326 : 163);
    selections++;
  }
  for (const mutate of [
    (r, v) => { v.ownerAcceptance = true; },
    (r, v) => { v.physicalDeviceEvidence = true; },
    (r, v) => { r.captures[0].fieldUnchanged = false; },
    (r, v) => { r.captures.reverse(); },
    (r, v) => { v.testExecutable.loadedSHA256 = '0'.repeat(64); },
    (r, v) => { r.fixtureVersion = 'wrong'; },
  ]) {
    const r = structuredClone(record), v = structuredClone(verification);
    mutate(r, v);
    assert.throws(() => gallery.validateEvidence(r, v, id));
    rejected++;
  }
  assert.throws(() => gallery.validateEvidence(record, verification, id === 'v4' ? 'v5' : 'v4'));
  rejected++;
}
assert.throws(() => gallery.captureConfig('1040'));
assert.equal(gallery.DEFAULT_CAPTURE, 'v6');
assert.deepEqual(Object.keys(gallery.CAPTURES).sort(), ['v4', 'v5', 'v6']);
assert.equal(gallery.captureConfig('v6').root, '../../scene-qa-framing-20261116/native-capture-v6/');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
assert.match(html, /<option value="v6" selected>[^<]*pending evidence verification<\/option>/);
assert.doesNotMatch(html, /<option value="v[45]" selected>/, 'Earlier captures must not be selected by default');

// In-memory protocol fixture only, NOT new native evidence or a v6 capture claim.
const v5Root = path.resolve(__dirname, gallery.captureConfig('v5').root);
const syntheticRecord = JSON.parse(fs.readFileSync(path.join(v5Root, 'source-scene-records.json')));
const syntheticVerification = JSON.parse(fs.readFileSync(path.join(v5Root, 'verification.json')));
const v6 = gallery.captureConfig('v6');
assert.equal(v6.version, 'source-scene-qa-006-control-framing');
assert.equal(v6.recordSchema, 'source-scene-records-006');
assert.equal(gallery.STATUS, 'NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE');
syntheticRecord.fixtureVersion = syntheticVerification.fixtureVersion = v6.version;
syntheticRecord.schema = v6.recordSchema;
assert.equal(gallery.validateEvidence(syntheticRecord, syntheticVerification, 'v6').length, 18);
let v6Rejected = 0;
for (const mutate of [
  (r, v) => { r.fixtureVersion = gallery.captureConfig('v5').version; },
  (r, v) => { v.fixtureVersion = gallery.captureConfig('v5').version; },
  (r, v) => { r.fixtureVersion = v.fixtureVersion = 'wrong'; },
  (r, v) => { r.schema = 'source-scene-records-005'; },
  (r, v) => { r.status = 'PENDING'; },
  (r, v) => { v.status = 'PENDING'; },
  (r, v) => { r.captures[0].name = 'source-scene-candidate-ordinary-z100'; },
  (r, v) => { r.captures[0].pngSHA256['-native'] = '0'.repeat(64); },
  (r, v) => { v.files[r.captures[0].name + '-native.png'] = '0'.repeat(64); },
  (r, v) => { r.inputSHA256 = '0'.repeat(64); },
  (r, v) => { v.harnessSourceReadSHA256 = '0'.repeat(64); },
  (r, v) => { v.testExecutable.expectedBuildSHA256 = '0'.repeat(64); },
  (r, v) => { v.ownerAcceptance = true; },
]) {
  const r = structuredClone(syntheticRecord), v = structuredClone(syntheticVerification);
  mutate(r, v);
  assert.throws(() => gallery.validateEvidence(r, v, 'v6'));
  v6Rejected++;
}
for (const id of ['v4', 'v5']) {
  assert.throws(() => gallery.validateEvidence(syntheticRecord, syntheticVerification, id));
  v6Rejected++;
}
console.log(JSON.stringify({result:'PASS', actualCaptureVersions:actualIDs.length, images, selections,
  rejectedMutations:rejected+1, syntheticV6RejectedMutations:v6Rejected,
  v6NativeEvidence:actualIDs.includes('v6'), browserEvidence:false}));
