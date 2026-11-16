'use strict';
// Offline contract/mutation checks against real imported records. Not browser evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const gallery = require('./gallery.js');
const root = path.resolve(__dirname, gallery.captureConfig('1020').root);
const recordsPath = path.join(root, 'source-scene-records.json');
const verificationPath = path.join(root, 'verification.json');
assert.ok(fs.existsSync(recordsPath) && fs.existsSync(verificationPath), 'Real evidence absent: contract test requires imported files, no substitute');
const record = JSON.parse(fs.readFileSync(recordsPath));
const verification = JSON.parse(fs.readFileSync(verificationPath));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const files = gallery.validateEvidence(record, verification, '1020');
assert.equal(files.length, 18);
assert.equal(hash(fs.readFileSync(recordsPath)), verification.files['source-scene-records.json']);
for (const file of files) {
  const png = fs.readFileSync(path.join(root, file.name));
  assert.equal(hash(png), file.digest);
  assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
  assert.deepEqual([png.readUInt32BE(16), png.readUInt32BE(20)], file.pixels);
}
let combinations = 0;
for (const capture of record.captures) {
  for (const size of ['native', 'half']) {
    for (const gray of [false, true]) {
      const selected = gallery.selectedImage(capture, size, gray);
      assert.ok(files.some(file => file.name === selected.name));
      assert.deepEqual([selected.width, selected.height], size === 'half' ? [352, 163] : [704, 326]);
      assert.ok(selected.name.endsWith(gray ? '-grayscale.png' : `-${size}.png`));
      combinations++;
    }
  }
}
const mutations = [
  (r,v) => { v.status = 'ACCEPTED'; },
  (r,v) => { v.nativeTests = 0; },
  (r,v) => { v.images = 17; },
  (r,v) => { v.ownerAcceptance = true; },
  (r,v) => { r.captures.pop(); },
  (r,v) => { r.captures[0] = r.captures[1]; },
  (r,v) => { r.captures[0].name = '../outside'; },
  (r,v) => { r.captures[0].fieldUnchanged = false; },
  (r,v) => { r.captures[0].nativePixels = [700,326]; },
  (r,v) => { delete r.captures[0].pngSHA256['-half']; },
  (r,v) => { v.files[files[0].name] = '0'.repeat(64); },
  (r,v) => { v.testExecutable.loadedSHA256 = '0'.repeat(64); }
];
for (const mutate of mutations) {
  const changedRecord = structuredClone(record);
  const changedVerification = structuredClone(verification);
  mutate(changedRecord, changedVerification);
  assert.throws(() => gallery.validateEvidence(changedRecord, changedVerification, '1020'));
}
console.log(JSON.stringify({ offlineContract: 'PASS', captures: 6, imageHashesAndDimensions: 18, logicalSelectionCombinations: combinations, rejectedMutations: mutations.length, browserEvidence: false, nativeExecutionPerformed: false }));
