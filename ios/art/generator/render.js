const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const dir='/home/claude/lb_art/ios/';
  const list = process.argv.slice(2);
  for (const a of list) { const [n,w,h,t]=a.split(':'); const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:2}); await p.goto('file://'+dir+n+'.html'); await p.waitForTimeout(120); await p.screenshot({path:dir+n+'.png',omitBackground:t==='t'}); await p.close(); }
  await b.close();
})();
