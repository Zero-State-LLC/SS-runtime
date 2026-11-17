'use strict';
// Defect254: in-memory native-shaped protocol fixtures only. Never written as native evidence.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const g = require('./gallery.js');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const clone = x => JSON.parse(JSON.stringify(x));
const planURL = '../../footprint-ground-repair-20261116/plan/plan.json';
const repositoryURL = name => '../../../../' + name;
function readInto(map,url) { const bytes=fs.readFileSync(path.resolve(__dirname,url)); map.set(url,bytes); return bytes; }
function loadSupplements(map,record,assembly) {
  const binding=g.validateSupplements(record,assembly);
  const manifest=JSON.parse(readInto(map,repositoryURL(binding.manifest.path)));
  for(const dep of g.supplementalDependencies(record,assembly,manifest)) readInto(map,repositoryURL(dep.path));
  return manifest;
}
function packet(id) {
  const config = g.captureConfig(id), map = new Map();
  const read = url => readInto(map,url);
  const rb = read(config.root + 'source-scene-records.json');
  const record = JSON.parse(rb), verification = JSON.parse(read(config.root + 'verification.json'));
  const ab = read(config.assembly), assembly = JSON.parse(ab);
  const input=JSON.parse(read(config.input)); read(config.harness);
  for (const source of g.validateSources(record,assembly)) read(repositoryURL(source.path));
  for (const file of g.validateEvidence(record,verification,id)) read(config.root + file.name);
  if (id === 'v8' || id === 'v9') {
    read(g.captureConfig(id === 'v9' ? 'v8' : 'v7').root + 'source-scene-records.json');
    read(planURL);
  }
  const manifest=id==='v9'?loadSupplements(map,record,assembly):null;
  return {map,record,verification,assembly,input,manifest,rb,ab};
}
function nativeSupplement(sprite) {
  return {role:sprite.id,nodeName:'supplement-'+sprite.id,file:sprite.id+'.png',sha256:sprite.image.sha256,registration:clone(sprite.registration),
    verticesWorldXYZ:sprite.geometryLandmarks.map(v=>v.worldXYZ),verticesPixelsTopLeft:sprite.geometryLandmarks.map(v=>v.sourcePixelsTopLeft),footprintWorld:[...sprite.worldBoundsXYZ.min.slice(0,2),...sprite.worldBoundsXYZ.max.slice(0,2)]};
}
function syntheticV9() {
  const base=packet('v8'),record=clone(base.record),verification=clone(base.verification),assembly=clone(base.assembly),input=clone(base.input);
  const config=g.captureConfig('v9'),old=g.captureConfig('v8'),map=new Map();
  const manifest=JSON.parse(readInto(map,repositoryURL(g.FINAL_SOURCE+'manifest.json')));
  const evidence='docs/review/blocked-base-curb-relief-20261116/SOURCE-REVIEW-FINAL.md';
  const evidenceBytes=readInto(map,repositoryURL(evidence));
  assembly.schema='blocked-base-curb-assembly-009';
  record.fixtureVersion=verification.fixtureVersion=assembly.fixtureVersion=config.version;
  record.schema=config.recordSchema;record.baselineRecordSHA256=assembly.baselineRecordSHA256=old.recordHash;
  record.supplementalManifestSHA256=g.FINAL_MANIFEST_SHA256;
  assembly.supplementalBinding={schema:'blocked-base-curb-recommendations-009',manifest:{path:g.FINAL_SOURCE+'manifest.json',sha256:g.FINAL_MANIFEST_SHA256},
    dependencies:Object.keys(manifest.files).sort().map(name=>({path:g.FINAL_SOURCE+name,sha256:manifest.files[name]})),
    recommendation:{reviewerRole:'coordinator',decision:'recommended',scope:'isolated-ordinary-scene',manifestSHA256:g.FINAL_MANIFEST_SHA256,evidence:{path:evidence,sha256:sha(evidenceBytes)}}};
  assembly.supplements=manifest.sprites.map(nativeSupplement);
  record.loadedTestExecutable.sha256=verification.testExecutable.loadedSHA256=verification.testExecutable.expectedBuildSHA256=sha('IN-MEMORY SYNTHETIC V9 binary, not native evidence');
  // Both arms start from the actual V8 candidate, as the Swift fixture does.
  record.captures=record.captures.map(row=>{
    const c=clone(base.record.captures.find(c=>c.arm==='candidate' && c.zoom===row.zoom));
    c.arm=row.arm;c.name=row.name;c.comparisonRole=c.arm==='control'?'BASELINE_V8_CANDIDATE':'CANDIDATE_V9_BASE_CURB_RELIEF';
    const supplements=c.arm==='candidate'?assembly.supplements:[];
    c.uprightCount=18;c.supplementalCount=supplements.length;c.totalPresentationUprightCount=18+supplements.length;
    c.supplementalActors=supplements.map(s=>({ ...clone(c.actors[0]),name:s.nodeName,worldRoot:s.registration.worldPosition,size:s.registration.drawSizeWorld,
      anchor:[s.registration.rootPixelsTopLeft[0]/s.registration.canvasPixels[0],1-s.registration.rootPixelsTopLeft[1]/s.registration.canvasPixels[1]] }));
    c.supplementalSourceWitnesses=supplements.map(s=>({nodeName:s.nodeName,role:s.role,sourceSHA256:s.sha256,footprintWorld:s.footprintWorld,
      vertices:s.verticesWorldXYZ.map((xyz,i)=>({worldXYZ:xyz,sourcePixelsTopLeft:s.verticesPixelsTopLeft[i],projectedSource:[0,0],projectedWorldXYZ:[0,0]}))}));
    for(const suffix of ['-native','-half','-grayscale']){
      const bytes=base.map.get(old.root+`source-scene-candidate-ordinary-z${Math.round(c.zoom*100)}`+suffix+'.png');
      map.set(config.root+c.name+suffix+'.png',bytes);c.pngSHA256[suffix]=sha(bytes);verification.files[c.name+suffix+'.png']=sha(bytes);
    }
    return c;
  });
  for(const source of assembly.sources) map.set(repositoryURL(source.image.path),base.map.get(repositoryURL(source.image.path)));
  map.set(planURL,base.map.get(planURL));map.set(old.root+'source-scene-records.json',base.rb);
  const harness=readInto(map,config.harness);record.harnessSourceReadSHA256=verification.harnessSourceReadSHA256=sha(harness);
  const ab=Buffer.from(JSON.stringify(assembly));record.assemblySHA256=sha(ab);map.set(config.assembly,ab);
  Object.assign(input,{schema:'source-scene-native-009',fixtureVersion:config.version,assemblySHA256:sha(ab),harnessSourceSHA256:sha(harness),baselineRecordSHA256:old.recordHash,
    supplementalBinding:assembly.supplementalBinding,supplements:assembly.supplements,supplementalManifestSHA256:g.FINAL_MANIFEST_SHA256});
  const ib=Buffer.from(JSON.stringify(input));map.set(config.input,ib);record.inputSHA256=verification.inputSHA256=sha(ib);
  const rb=Buffer.from(JSON.stringify(record));verification.files['source-scene-records.json']=sha(rb);
  map.set(config.root+'source-scene-records.json',rb);map.set(config.root+'verification.json',Buffer.from(JSON.stringify(verification)));
  loadSupplements(map,record,assembly);
  return {map,record,verification,assembly,input,manifest,rb,ab};
}
function documents(p) {
  return new Map([...p.map].filter(([url])=>url.startsWith('../../../../')&&url.endsWith('.json')).map(([url,bytes])=>[url.slice(12),JSON.parse(bytes)]));
}
module.exports={sha,clone,packet,syntheticV9,planURL,repositoryURL,documents};
