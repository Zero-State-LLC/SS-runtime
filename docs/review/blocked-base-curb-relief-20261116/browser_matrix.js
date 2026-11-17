// Execute only in the actual local V9 gallery via browser bridge.
// This exercises real DOM controls and image load events, not a mock DOM.
return (async () => {
  const el = id => document.getElementById(id);
  const need = (value, message) => { if (!value) throw new Error(message); };
  const waitFor = predicate => new Promise((resolve, reject) => {
    if (predicate()) return resolve();
    const observer = new MutationObserver(() => {
      if (predicate()) { observer.disconnect(); clearTimeout(timer); resolve(); }
    });
    const timer = setTimeout(() => { observer.disconnect(); reject(new Error('DOM evidence load deadline')); }, 60000);
    observer.observe(document.body, {subtree:true, childList:true, attributes:true, characterData:true});
  });
  const loaded = image => new Promise((resolve, reject) => {
    if (image.complete) return image.naturalWidth ? resolve() : reject(new Error('Broken image'));
    image.addEventListener('load', resolve, {once:true});
    image.addEventListener('error', () => reject(new Error('Image load failed')), {once:true});
  });
  const change = (id, value) => {
    if (id === 'grayscale') el(id).checked = value;
    else el(id).value = value;
    el(id).dispatchEvent(new Event('change', {bubbles:true}));
  };
  let selections = 0, imageDisplays = 0;
  const versions = [];
  for (const version of ['v8','v9']) {
    change('capture', version);
    await waitFor(() => el('status').textContent.startsWith('Importer-verified evidence loaded') && el('captures').querySelectorAll('img').length > 0);
    need(el('capture').value === version, 'Capture substitution');
    for (const zoom of ['1','1.25','1.4']) for (const arm of ['paired','baseline','candidate']) for (const size of ['native','half']) for (const gray of [false,true]) {
      change('zoom', zoom); change('arm', arm); change('size', size); change('grayscale', gray);
      const images = [...el('captures').querySelectorAll('img')];
      need(images.length === (arm === 'paired' ? 2 : 1), 'Wrong image census');
      await Promise.all(images.map(loaded));
      for (const image of images) {
        const box = image.getBoundingClientRect();
        need(box.width === (size === 'native' ? 704 : 352) && box.height === (size === 'native' ? 326 : 163), 'Logical size drift');
        need(image.naturalWidth > 0 && image.naturalHeight > 0, 'Empty native image');
        const suffix = gray ? '-grayscale.png' : size === 'half' ? '-half.png' : '-native.png';
        need(image.dataset.evidenceFile.endsWith(suffix), 'Wrong evidence image variant');
        need(image.dataset.evidenceFile.includes('-z' + Math.round(Number(zoom)*100) + '-'), 'Wrong zoom image');
        imageDisplays++;
      }
      need(el('benchmark').classList.contains('grayscale') === gray, 'Reference grayscale state drift');
      need(getComputedStyle(el('benchmark')).filter === (gray ? 'grayscale(1)' : 'none'), 'Reference grayscale filter drift');
      selections++;
    }
    versions.push({version, status:el('status').textContent});
  }
  change('capture','v9');
  await waitFor(() => el('status').textContent.startsWith('Importer-verified evidence loaded') && el('captures').querySelectorAll('img').length > 0);
  change('zoom','1'); change('arm','candidate'); change('size','native'); change('grayscale',false);
  await Promise.all([...el('captures').querySelectorAll('img')].map(loaded));
  need(getComputedStyle(el('benchmark')).filter === 'none', 'Reference grayscale did not restore');
  const result = {status:'PASS', actualBrowser:true, url:location.href, selections, imageDisplays, versions, finalSelection:'v9/candidate/1/native/color', logicalSizes:[[704,326],[352,163]], referenceGrayscaleRestored:true, documentOverflow:document.documentElement.scrollWidth>innerWidth, nativeExecution:false, ownerAcceptance:false};
  window.v9BrowserMatrixResult = result;
  return result;
})();
