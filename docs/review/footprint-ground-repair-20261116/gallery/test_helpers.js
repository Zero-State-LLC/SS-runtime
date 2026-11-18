'use strict';
// Shared Node test helpers. Synthetic V8 records below are NEVER written as capture evidence.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const g = require('./gallery.js');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const clone = value => JSON.parse(JSON.stringify(value));
function packet(id) {
  const config = g.captureConfig(id), root = path.resolve(__dirname, config.root);
  const rb = fs.readFileSync(path.join(root, 'source-scene-records.json'));
  const vb = fs.readFileSync(path.join(root, 'verification.json'));
  const record = JSON.parse(rb), verification = JSON.parse(vb);
  const ab = fs.readFileSync(path.resolve(__dirname, config.assembly)), assembly = JSON.parse(ab);
  const map = new Map([[config.root + 'source-scene-records.json', rb], [config.root + 'verification.json', vb], [config.assembly, ab]]);
  for (const key of ['input','harness']) map.set(config[key],fs.readFileSync(path.resolve(__dirname,config[key])));
  for (const file of g.validateEvidence(record, verification, id)) map.set(config.root + file.name, fs.readFileSync(path.join(root, file.name)));
  for (const source of g.validateSources(record, assembly)) map.set('../../../../' + source.path, fs.readFileSync(path.resolve(__dirname, '../../../../', source.path)));
  if (id === 'v8') {
    map.set(g.captureConfig('v7').root + 'source-scene-records.json', packet('v7').rb);
    map.set('../plan/plan.json', fs.readFileSync(path.resolve(__dirname,'../plan/plan.json')));
  }
  return { record, verification, assembly, map, rb, ab };
}
function syntheticV8() {
  // Deliberately synthetic network-only protocol fixture. Old PNG bytes are reused
  // solely to test the loader. No file is created and no native result is claimed.
  const base = packet('v7'), record = clone(base.record), verification = clone(base.verification), assembly = clone(base.assembly);
  const config = g.captureConfig('v8'), old = g.captureConfig('v7');
  record.fixtureVersion = verification.fixtureVersion = assembly.fixtureVersion = config.version;
  record.schema = config.recordSchema;
  record.baselineRecordSHA256 = old.recordHash;
  const plan = Buffer.from('{"testOnly":"SYNTHETIC V8 protocol fixture"}');
  record.planSHA256 = sha(plan);
  const source = {role:'ground-plan',image:{path:'docs/review/SYNTHETIC-TEST-ONLY/ground.png',sha256:sha(plan)}};
  record.sourceSHA256['ground-plan'] = source.image.sha256;
  assembly.sources.push(source);
  record.loadedTestExecutable.sha256 = verification.testExecutable.loadedSHA256 = verification.testExecutable.expectedBuildSHA256 = sha('SYNTHETIC V8 executable');
  for (const c of record.captures) c.comparisonRole = c.arm === 'control' ? 'BASELINE_V7_CANDIDATE' : 'CANDIDATE_V8_SHARED_GROUND_PLAN';
  const ab = Buffer.from(JSON.stringify(assembly)); record.assemblySHA256 = sha(ab);
  const rb = Buffer.from(JSON.stringify(record)); verification.files['source-scene-records.json'] = sha(rb);
  const map = new Map([...base.map].map(([url,bytes]) => [url.replace(old.root,config.root),bytes]));
  map.delete(old.assembly);
  map.delete(old.input); map.delete(old.harness);
  map.set(config.input,base.map.get(old.input)); map.set(config.harness,base.map.get(old.harness));
  map.set(config.root + 'source-scene-records.json',rb);
  map.set(config.root + 'verification.json',Buffer.from(JSON.stringify(verification)));
  map.set(config.assembly,ab);
  map.set(old.root + 'source-scene-records.json',base.rb);
  map.set('../plan/plan.json',plan);
  map.set('../../../../' + source.image.path,plan);
  return {record,verification,assembly,map,rb,ab};
}
module.exports = { sha, clone, packet, syntheticV8 };
