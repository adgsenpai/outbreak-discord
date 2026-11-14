// Read-only DOM tracker and lobby inspection. Never touches game memory or network.
const ROOM_RE = /Area\s*(\d+)\s*·\s*([^·]+)\s*·\s*(\d+\s*\/\s*\d+)\s*players\s*·\s*(Public|Private)/i;
function snapshot() {
 const username = document.querySelector('#chat-info')?.textContent?.match(/writing as\s+([\w-]+)/i)?.[1] || document.querySelector('#name-hint')?.textContent?.match(/play as\s+([\w-]+)/i)?.[1] || '';
 const rooms = [...document.querySelectorAll('#rooms .room')].map(el=>{
   const metadata=[...el.querySelectorAll('.meta')].map(x=>x.textContent.trim()).join(' · ');
   const m=metadata.match(ROOM_RE);
   return {name:el.querySelector('b')?.textContent.trim().slice(0,80)||'',status:el.querySelector('.tag')?.textContent.trim().slice(0,32)||'',area:m?.[1]||'',players:m?.[3]?.replace(/\s/g,'')||'',visibility:m?.[4]||'',usernames:[...el.querySelectorAll('.who-n')].map(x=>x.textContent.trim())};
 });
 const cards=[...document.querySelectorAll('#trk-panel .trk-card')];
 const tracker=cards.length ? {
  characters:cards.map(c=>{const node=c.querySelector('.trk-name');const name=[...node?.childNodes||[]].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent).join('').trim();return {name:name.slice(0,32),location:c.querySelector('.trk-room')?.textContent.trim().slice(0,100)||'',health:c.querySelector('.trk-hp .trk-num')?.textContent.trim().slice(0,24)||'',virus:c.querySelector('.trk-vir')?.textContent.trim().slice(0,30)||''}}),
  difficulty:document.querySelector('#trk-panel .trk-foot .muted')?.textContent.trim().slice(0,24)||'',
  matchTime:document.querySelector('#trk-panel .trk-clock')?.textContent.trim().slice(0,30)||''
 } : null;
 return {username,rooms,tracker};
}
chrome.runtime.onMessage.addListener((msg,sender,reply)=>{if(msg?.type==='outbreak-snapshot')reply(snapshot())});
