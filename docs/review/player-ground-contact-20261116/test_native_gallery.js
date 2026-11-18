// Behavioral harness for the shipped inline gallery script, not browser/layout evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(__dirname + '/native-pairs.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const flush = () => new Promise(resolve => setImmediate(resolve));
function setup() {
  const pending = [], elements = {};
  for (const id of ['pair','size','gray','baseline','candidate','status','error'])
    elements[id] = { value: id === 'pair' ? '0' : 'large', checked: false, textContent: '', append() {} };
  const document = {body:{dataset:{},className:''},getElementById:id=>elements[id],createElement:()=>({})};
  class TestImage {
    constructor() { this.naturalWidth=480; }
    set src(value) { this.path=value;pending.push(this); }
    get src() { return this.path; }
    decode() { throw Error('Hidden-tab decode must not be awaited'); }
  }
  const window = {};
  vm.runInNewContext(script, {document,window,Image:TestImage,Promise,Error});
  return {pending,elements,document,api:window.nativeContactReview};
}
async function main() {
  let h=setup();
  assert.equal(h.api.pairs.length,38);
  for (const image of h.pending.splice(0)) image.onload();
  await flush();
  assert.equal(h.document.body.dataset.ready,'true');
  for (let i=0;i<38;i++) {
    h.elements.pair.value=String(i);
    const done=h.api.render();
    for (const image of h.pending.splice(0)) image.onload();
    await done;
    assert.equal(h.document.body.dataset.ready,'true');
    for (const family of ['baseline','candidate'])
      assert.equal(h.elements[family].src,'native/'+h.api.pairs[i][family]);
  }
  h=setup();
  h.pending[0].onerror();h.pending[1].onload();await flush();
  assert.equal(h.document.body.dataset.ready,'false');
  assert.match(h.elements.error.textContent,/FAILED:/);
  h=setup();
  h.pending[0].naturalWidth=0;
  h.pending.forEach(image=>image.onload());await flush();
  assert.equal(h.document.body.dataset.ready,'false');
  assert.match(h.elements.error.textContent,/Empty image/);
  for(const staleFailure of [false,true]) {
    h=setup();const stale=h.pending.splice(0);
    h.elements.pair.value='1';const done=h.api.render();
    h.pending.splice(0).forEach(image=>image.onload());await done;
    stale.forEach(image=>staleFailure?image.onerror():image.onload());await flush();
    assert.equal(h.document.body.dataset.ready,'true');
    assert.equal(h.elements.error.textContent,'');
    assert.equal(h.elements.baseline.src,'native/'+h.api.pairs[1].baseline);
  }
  h.elements.size.value='half';h.elements.gray.checked=true;h.elements.size.onchange();
  assert.equal(h.document.body.className,'half gray');
  console.log('PASS: 38 paired selections; missing/empty images fail closed; stale success/error cannot replace newer pair; size/grayscale control state.');
}
main().catch(error=>{console.error(error);process.exitCode=1;});
