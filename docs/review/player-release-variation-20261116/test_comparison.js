// Execute actual exported comparison code with RAF deliberately not called.
// Readiness/manual synchronization harness, not native/browser cadence evidence.
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');

for(const speed of ['normal','quarter']){
  for(const mode of ['cached','delayed','broken-cached','error-event']){
    test(`${speed}: ${mode} readiness without RAF/decode`,async()=>{
      const html=fs.readFileSync(path.join(__dirname,'artifacts',`${speed}-speed.html`),'utf8');
      const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
      const elements={};
      for(const id of ['status','pose','toggle','phase','baseline','candidate','contact','profile'])elements[id]={value:id==='phase'?'1':'0',disabled:true,textContent:'',src:'',href:''};
      const images=[];let rafCount=0,decodeCount=0;
      class TestImage{
        constructor(){this.complete=mode!=='delayed'&&mode!=='error-event';this.naturalWidth=mode==='broken-cached'?0:384;this.naturalHeight=416;images.push(this)}
        decode(){decodeCount++;return new Promise(()=>{})}
      }
      const document={getElementById:id=>elements[id],documentElement:{dataset:{}}};
      const context=vm.createContext({document,Image:TestImage,requestAnimationFrame:()=>rafCount++,console});
      vm.runInContext(script,context);
      assert.equal(images.length,544);
      if(mode==='delayed'){
        assert.equal(document.documentElement.dataset.reviewReady,'loading');
        images.forEach(im=>{im.complete=true;im.onload()});
      }else if(mode==='error-event')images[0].onerror();
      await new Promise(resolve=>setImmediate(resolve));
      assert.equal(decodeCount,0);
      if(mode==='broken-cached'||mode==='error-event'){
        assert.equal(document.documentElement.dataset.reviewReady,'error');
        assert.equal(elements.pose.disabled,true);assert.equal(elements.phase.disabled,true);
        assert.equal(rafCount,0);return;
      }
      assert.equal(document.documentElement.dataset.reviewReady,'true');
      assert.equal(rafCount,1);assert.equal(elements.pose.disabled,false);assert.equal(elements.phase.disabled,false);
      assert.equal(vm.runInContext('fps',context),speed==='normal'?128:32);
      for(let phase=1;phase<=16;phase++){
        elements.phase.value=String(phase);elements.phase.onchange();
        for(let pose=0;pose<=16;pose++){
          elements.pose.value=String(pose);elements.pose.oninput();
          const suffix=`phase-${String(phase).padStart(2,'0')}/frames/${String(pose).padStart(2,'0')}.png`;
          assert.equal(elements.baseline.src,`../../player-all-release-source-20261116/artifacts/${suffix}`);
          assert.equal(elements.candidate.src,`./${suffix}`);
          assert.match(elements.status.textContent,new RegExp(`synchronized pose ${pose}/16`));
        }
      }
      assert.equal(rafCount,1,'manual controls do not depend on executing RAF');
    });
  }
}
