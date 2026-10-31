const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const P='dw/project';const t=JSON.parse(fs.readFileSync(P+'/tokens.json'));
let css=':root{';for(const c of t.color.tokens){let v=typeof c.value=='string'?c.value:c.value.light;v=v.replace(/^\{(.*)\}$/,'var(--$1)');css+=`--${c.name}:${v};`}
for(const fam of ['spacing','radius','shadow'])for(const c of t[fam].tokens)css+=`--${c.name}:${c.value};`;
css+=`--font-sans:${t.type.families.sans};}`;
for(const g of t.type.groups)for(const s of g.styles)css+=`.${s.name}{font-family:var(--font-sans);font-size:${s.fontSize};line-height:${s.lineHeight};font-weight:${s.fontWeight};${s.letterSpacing?'letter-spacing:'+s.letterSpacing+';':''}}`;
const b=fs.readFileSync(P+'/components/bundle.css','utf8');
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1400,height:900}});
for(const d of fs.readdirSync(P+'/components')){const f=`${P}/components/${d}/preview.html`;if(!fs.existsSync(f))continue;
let h=fs.readFileSync(f,'utf8').replace('<head>',`<head><style>${css}</style><style>${b}</style>`);
fs.writeFileSync('out_'+d+'.html',h);await pg.goto('file://'+path.resolve('out_'+d+'.html'));await pg.waitForTimeout(300);
await pg.screenshot({path:`shot_${d}.png`,fullPage:true});
const o=await pg.evaluate(()=>[...document.querySelectorAll('.dw-phone:not(.is-long) .dw-body')].map(e=>e.scrollHeight-e.clientHeight));console.log(d,o);}
await br.close();})();
