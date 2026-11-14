// Read-only DOM tracker and lobby inspection. Never touches game memory or network.
const ROOM_RE = /Area\s*(\d+)\s*·\s*([^·]+)\s*·\s*(\d+\s*\/\s*\d+)\s*players\s*·\s*(Public|Private)/i;
// Latest numbers from page-bridge.js (scenario id, room id) — the site's own tracker state.
let gameState = null;
window.addEventListener('message', e => {
 if (e.source !== window || e.data?.source !== 'outbreak-discord-bridge') return;
 const d = e.data;
 gameState = d.state === 'game' ? {scen: Number.isInteger(d.scen) ? d.scen : null, room: Number.isInteger(d.room) ? d.room : null, diff: Number.isInteger(d.diff) ? d.diff : null, at: Date.now()} : null;
});
function snapshot() {
 const username = document.querySelector('#chat-info')?.textContent?.match(/writing as\s+([\w-]+)/i)?.[1] || document.querySelector('#name-hint')?.textContent?.match(/play as\s+([\w-]+)/i)?.[1] || '';
 const rooms = [...document.querySelectorAll('#rooms .room')].map(el=>{
   const metadata=[...el.querySelectorAll('.meta')].map(x=>x.textContent.trim()).join(' · ');
   const m=metadata.match(ROOM_RE);
   return {name:el.querySelector('b')?.textContent.trim().slice(0,80)||'',status:el.querySelector('.tag')?.textContent.trim().slice(0,32)||'',area:m?.[1]||'',players:m?.[3]?.replace(/\s/g,'')||'',visibility:m?.[4]||'',usernames:[...el.querySelectorAll('.who-n')].map(x=>x.textContent.trim())};
 });
 // The site renders cards into the side panel and/or the in-game overlay; read whichever has them.
 let cards=[...document.querySelectorAll('#trk-panel .trk-card')];
 if(!cards.length)cards=[...document.querySelectorAll('#trk-ov .trk-card')];
 const live=gameState&&Date.now()-gameState.at<10000?gameState:null;
 const tracker=(cards.length||live) ? {
  scen:live?.scen??null, roomId:live?.room??null,
  characters:cards.map(c=>{const node=c.querySelector('.trk-name');const name=[...node?.childNodes||[]].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent).join('').trim();return {name:name.slice(0,32),location:c.querySelector('.trk-room')?.textContent.trim().slice(0,100)||'',health:c.querySelector('.trk-hp .trk-num')?.textContent.trim().slice(0,24)||'',virus:c.querySelector('.trk-vir')?.textContent.trim().slice(0,30)||''}}),
  difficulty:document.querySelector('#trk-panel .trk-foot .muted')?.textContent.trim().slice(0,24)||'',
  matchTime:document.querySelector('#trk-panel .trk-clock')?.textContent.trim().slice(0,30)||''
 } : null;
 return {username,rooms,tracker};
}
chrome.runtime.onMessage.addListener((msg,sender,reply)=>{if(msg?.type==='outbreak-snapshot')reply(snapshot())});
