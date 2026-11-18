'use strict';
// ADAPT: footprint-ground-repair-20261116/gallery/test_evidence.js:1-127.
// Retained-byte/protocol checks. Synthetic V9 never substitutes for native evidence.
const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path');
const g=require('./gallery.js');
const {packet,syntheticV9,sha,clone,planURL,documents,repositoryURL}=require('./test_helpers.js');
async function main(){
assert.equal(g.DEFAULT_CAPTURE,'v9');
assert.throws(()=>g.captureConfig('../escape'));
let actual=0,images=0,rejected=0,selections=0;
const ids=['v7','v8'];
if(fs.existsSync(path.resolve(__dirname,g.captureConfig('v9').root,'verification.json'))) ids.push('v9');
else assert.ok(!process.argv.includes('--require-v9'),'Actual V9 evidence required, not synthetic substitute');
const entries=[...ids.map(id=>({id,p:packet(id),native:true})),{id:'v9',p:syntheticV9(),native:false}];
for(const {id,p,native} of entries){
 const {record:r,verification:v,assembly:a}=p,config=g.captureConfig(id);
 const files=g.validateEvidence(r,v,id);
 assert.equal(sha(p.rb),v.files['source-scene-records.json']);
 if(config.recordHash)assert.equal(sha(p.rb),config.recordHash);
 assert.equal(sha(p.ab),r.assemblySHA256);
 for(const [file,digest] of [[config.input,r.inputSHA256],[config.harness,r.harnessSourceReadSHA256]])assert.equal(sha(p.map.get(file)),digest);
 if(id!=='v7'){assert.equal(sha(p.map.get(planURL)),r.planSHA256);g.validateBaseline(r,packet(id==='v9'?'v8':'v7').record);}
 for(const s of g.validateSources(r,a))assert.equal(sha(p.map.get('../../../../'+s.path)),s.sha256);
 if(id==='v9'){
  assert.equal(a.sources.length,10);assert.equal(Object.keys(r.sourceSHA256).length,10);
  assert.equal(Object.hasOwn(r,'supplementalSource'),false);
  for(const s of g.supplementalDependencies(r,a,p.manifest))assert.equal(sha(p.map.get(repositoryURL(s.path))),s.sha256);
  assert.equal(g.validateSupplementPayload(r,a,p.manifest,documents(p),p.input).length,53);
  assert.equal((await g.verifySupplementalEvidence(r,a,p.input,async url=>{assert.ok(p.map.has(url),url);return p.map.get(url);})).length,53);
 }
 for(const f of files){const png=p.map.get(config.root+f.name);assert.equal(sha(png),f.digest);assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([png.readUInt32BE(16),png.readUInt32BE(20)],f.pixels);if(native)images++;}
 for(const c of r.captures)for(const size of ['native','half'])for(const gray of [false,true]){const selected=g.selectedImage(c,size,gray);assert.ok(files.some(f=>f.name===selected.name));assert.equal(selected.width,size==='native'?704:352);assert.equal(selected.height,size==='native'?326:163);selections++;}
 const mutations=[
  (r,v)=>r.schema='unknown',(r,v)=>r.fixtureVersion='wrong',(r,v)=>v.fixtureVersion='wrong',
  (r,v)=>v.status='ACCEPTED',(r,v)=>r.status='ACCEPTED',(r,v)=>v.nativeTests=0,(r,v)=>v.captures=5,(r,v)=>v.images=17,
  (r,v)=>v.ownerAcceptance=true,(r,v)=>v.physicalDeviceEvidence=true,(r,v)=>v.animationFamilyEvidence=true,
  (r,v)=>r.ownerAcceptance=true,(r,v)=>r.physicalDeviceEvidence=true,(r,v)=>r.animationFamilyEvidence=true,
  (r,v)=>r.inputSHA256='0'.repeat(64),(r,v)=>r.harnessSourceReadSHA256='0'.repeat(64),
  (r,v)=>v.testExecutable.expectedBuildSHA256='0'.repeat(64),(r,v)=>r.loadedTestExecutable.sha256='0'.repeat(64),
  (r,v)=>r.captures.pop(),(r,v)=>r.captures[0].name='../escape',(r,v)=>r.captures[0].arm='wrong',
  (r,v)=>r.captures[0].authorityAfter='changed',(r,v)=>r.captures[0].fieldUnchanged=false,
  (r,v)=>r.captures[0].nativePixels=[704,325],(r,v)=>r.captures[0].pngSHA256['-native']='0'.repeat(64),
  (r,v)=>delete v.files['source-scene-records.json'],(r,v)=>v.files['extra.png']='0'.repeat(64),
  (r,v)=>r.baselineRecordSHA256='0'.repeat(64),(r,v)=>r.sourceSHA256.kiosk='invalid',
  (r,v)=>r.captures[0].comparisonRole='ORIGINAL',(r,v)=>r.captures[0].solidCount=23,
  (r,v)=>r.syntheticFixture=true
 ];
 if(id==='v9')mutations.push((r,v)=>delete r.supplementalManifestSHA256,(r,v)=>r.supplementalManifestSHA256='0'.repeat(64),(r,v)=>r.supplementalSource={},(r,v)=>r.sourceSHA256['invented-extra']='0'.repeat(64),
  (r,v)=>r.captures[3].supplementalCount=52,(r,v)=>r.captures[3].supplementalSourceWitnesses.pop(),(r,v)=>r.captures[0].supplementalActors.push({name:'invented'}));
 for(const change of mutations){const rr=clone(r),vv=clone(v);change(rr,vv);assert.throws(()=>g.validateEvidence(rr,vv,id));rejected++;}
 for(const change of [a=>a.sources.pop(),a=>a.sources.push(a.sources[0]),a=>a.sources[0].image.path='docs/review/../../escape']){const aa=clone(a);change(aa);assert.throws(()=>g.validateSources(r,aa));rejected++;}
 if(id!=='v7')for(const change of [r=>r.sourceSHA256.camera='0'.repeat(64),r=>r.loadedTestExecutable.sha256=packet(id==='v9'?'v8':'v7').record.loadedTestExecutable.sha256]){const rr=clone(r);change(rr);assert.throws(()=>g.validateBaseline(rr,packet(id==='v9'?'v8':'v7').record));rejected++;}
 if(id==='v9'){
  const changes=[
   x=>delete x.assembly.supplementalBinding,
   x=>delete x.assembly.supplementalBinding.dependencies,
   x=>x.assembly.supplementalBinding.dependencies.pop(),
   x=>x.assembly.supplementalBinding.dependencies.push(x.assembly.supplementalBinding.dependencies[0]),
   x=>x.assembly.supplementalBinding.dependencies[0].sha256='0'.repeat(64),
   x=>x.assembly.supplementalBinding.manifest.path=g.SOURCE_ROOT+'manifest.json',
   x=>x.assembly.supplementalBinding.manifest.sha256='49939b540e47b6c87a777e940a60add957c12013fbb1c6237f9794f8b32aa5e6',
   x=>x.assembly.supplementalBinding.recommendation.decision='pending',
   x=>x.assembly.supplementalBinding.recommendation.reviewerRole='source-worker',
   x=>x.assembly.supplementalBinding.recommendation.scope='production',
   x=>x.assembly.supplementalBinding.recommendation.manifestSHA256='0'.repeat(64),
   x=>delete x.assembly.supplementalBinding.recommendation.evidence,
   x=>x.assembly.supplementalBinding.recommendation.evidence.path=g.SOURCE_ROOT+'attempt-01/source-snapshot/README.md',
   x=>x.assembly.supplementalBinding.recommendation.evidence.path=g.FINAL_SOURCE+'README.md',
   x=>x.assembly.supplements[0].sha256='0'.repeat(64),
   x=>x.assembly.supplements[0].registration.worldPosition[0]+=1,
   x=>x.assembly.supplements[0].verticesWorldXYZ[0][2]+=1,
   x=>x.assembly.sources.push(clone(x.assembly.sources[0])),
   x=>x.assembly.viewCenterWorld[0]+=1,
   x=>x.manifest.attempt=1,
   x=>x.manifest.files['geometry.json']='0'.repeat(64),
   x=>x.manifest.sprites[0].image.path=g.SOURCE_ROOT+'attempt-01/sprites/v9-blocked-kiosk-base.png',
   x=>x.record.captures[3].supplementalSourceWitnesses[0].sourceSHA256='0'.repeat(64),
   x=>x.record.captures[3].supplementalSourceWitnesses[0].vertices[0].worldXYZ[2]+=1,
   x=>x.input.supplementalManifestSHA256='0'.repeat(64),
   x=>x.input.supplements.pop(),
   x=>x.input.sources[0].sha256='0'.repeat(64)
  ];
  for(const unsafe of ['../escape','/escape','docs//escape','docs/./escape','docs/%2e%2e/escape','docs\\escape']) changes.push(x=>x.assembly.supplementalBinding.dependencies[0].path=unsafe);
  for(const change of changes){const x=clone({record:r,assembly:a,manifest:p.manifest,input:p.input});change(x);assert.throws(()=>g.validateSupplementPayload(x.record,x.assembly,x.manifest,documents(p),x.input));rejected++;}
  for(const name of [g.FINAL_SOURCE+'geometry.json',g.FINAL_SOURCE+'output/registration.json',g.FINAL_SOURCE+'attempt-01-frozen-sha256.json',g.SOURCE_ROOT+'geometry.json',g.V8_DIRECTORY+'scene/assembly.json']){
   const docs=documents(p);docs.delete(name);assert.throws(()=>g.validateSupplementPayload(r,a,p.manifest,docs,p.input));rejected++;
  }
  const sourceURL=repositoryURL(p.manifest.sprites[0].image.path);
  const changed=new Map(p.map);changed.set(sourceURL,Buffer.from('corrupt final source'));
  await assert.rejects(()=>g.verifySupplementalEvidence(r,a,p.input,async url=>changed.get(url)),/Supplemental bytes differ/);rejected++;
 }
 if(native)actual++;
}
assert.throws(()=>g.selectedImage({name:'none'},'stretch',false));
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
assert.match(html,/value="v9" selected/);assert.doesNotMatch(html,/value="v8" selected/);
assert.match(html,/baselineV8 versus candidateV9/);assert.match(html,/Review only\. Overall benchmark NOT MET\. V8 and V9 are unaccepted/);
console.log(JSON.stringify({result:'PASS',actualVersions:actual,actualImages:images,selections,rejectedMutations:rejected,syntheticV9Protocol:true,v9NativeEvidence:ids.includes('v9'),browserEvidence:false}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
