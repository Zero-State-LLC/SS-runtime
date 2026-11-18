#!/usr/bin/env node
// Exercise the actual generated page script with RAF deliberately never executed.
// This is a readiness regression harness, not browser/native cadence evidence.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');

async function check(file, mode) {
  const script = fs.readFileSync(file, 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
  const nodes = Array.from({length: 16}, (_, i) => ({dataset: {phase: String(i + 1)}}));
  const controls = {status: {textContent: 'Loading'}, pose: {disabled: true, value: '0'}, toggle: {disabled: true}};
  const images = [];
  let rafCalls = 0;
  let decodeCalls = 0;
  class FakeImage {
    constructor() {
      this.complete = mode === 'cached' || mode === 'cached-broken';
      this.naturalWidth = mode === 'cached' ? 384 : 0;
      this.naturalHeight = mode === 'cached' ? 416 : 0;
      images.push(this);
    }
    decode() { decodeCalls++; return new Promise(() => {}); }
  }
  const document = {documentElement: {dataset: {}}, querySelectorAll: () => nodes, getElementById: id => controls[id]};
  vm.runInNewContext(script, {document, Image: FakeImage, requestAnimationFrame: () => { rafCalls++; }, Promise, Error});
  assert.equal(images.length, 272);
  if (mode === 'delayed' || mode === 'load-error') {
    assert.equal(document.documentElement.dataset.reviewReady, 'loading');
    assert.equal(controls.pose.disabled, true);
    images.forEach((image, i) => {
      if (mode === 'load-error' && i === 73) image.onerror();
      else { image.complete = true; image.naturalWidth = 384; image.naturalHeight = 416; image.onload(); }
    });
  }
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(decodeCalls, 0, 'Readiness must not await Image.decode');
  if (mode === 'cached-broken' || mode === 'load-error') {
    assert.equal(document.documentElement.dataset.reviewReady, 'error');
    assert.equal(controls.toggle.disabled, true);
    assert.equal(controls.pose.disabled, true);
    assert.equal(rafCalls, 0);
  } else {
    assert.equal(document.documentElement.dataset.reviewReady, 'true');
    assert.match(controls.status.textContent, /Ready: manual inspection available/);
    assert.equal(controls.toggle.disabled, false);
    assert.equal(controls.pose.disabled, false);
    assert.equal(rafCalls, 1, 'Ready is exposed before any RAF callback runs');
    controls.pose.value = '16'; controls.pose.oninput();
    assert(nodes.every(node => node.src.endsWith('/16.png')));
    assert.match(controls.status.textContent, /manual contact inspection/);
  }
  console.log(`PASS ${path.basename(file)} ${mode}`);
}

(async () => {
  const root = process.argv[2] || path.join(__dirname, 'artifacts');
  for (const page of ['normal-speed.html', 'quarter-speed.html']) {
    for (const mode of ['cached', 'delayed', 'cached-broken', 'load-error']) await check(path.join(root, page), mode);
  }
  console.log('8 readiness regressions passed, no skips');
})().catch(error => { console.error(error); process.exitCode = 1; });
