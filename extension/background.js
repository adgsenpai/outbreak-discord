const API = 'http://127.0.0.1:8766/status';
const TARGET = /^https:\/\/outbreakweb\.com\/(file1|file2)(?:\/|\?|#|$)/i;
let busy = false;
async function sync() {
  if (busy) return;
  busy = true;
  try {
    const {enabled=true, token='', username='', shareRoom=false} = await chrome.storage.local.get(['enabled','token','username','shareRoom']);
    const windows = await chrome.windows.getAll({populate:true});
    const tab = windows.filter(w=>w.focused).flatMap(w=>w.tabs||[]).find(t=>t.active && TARGET.test(t.url||''));
    const playing = Boolean(enabled && tab);
    const game = playing ? tab.url.match(TARGET)[1] : null;
    let room=null, tracker=null;
    if(playing){
      try {
        const snap=await chrome.tabs.sendMessage(tab.id,{type:'outbreak-snapshot'});
        tracker=snap?.tracker||null;
        const player=(username.trim()||snap?.username||'').toLowerCase();
        if(shareRoom && player)room=snap?.rooms?.find(r=>r.usernames.some(n=>n.toLowerCase()===player))||null;
      }catch(_){ /* Page may be loading */ }
    }
    const response = await fetch(API, {
      method:'POST',
      headers:{'Content-Type':'application/json','X-Outbreak-Token':token},
      body:JSON.stringify({playing,game,room,tracker}),
      signal:AbortSignal.timeout(2500)
    });
    await chrome.storage.local.set({connected:response.ok,playing:response.ok&&playing,game,room,tracker,lastError:response.ok?'':`HTTP ${response.status}`});
  } catch(err) {
    await chrome.storage.local.set({connected:false,playing:false,lastError:String(err)});
  } finally {busy=false;}
}
function init() {chrome.alarms.create('outbreak-sync',{periodInMinutes:0.5});sync();}
chrome.runtime.onInstalled.addListener(init);
chrome.runtime.onStartup.addListener(init);
chrome.alarms.onAlarm.addListener(a=>{if(a.name==='outbreak-sync')sync();});
chrome.tabs.onActivated.addListener(sync);
chrome.tabs.onUpdated.addListener((id,change)=>{if(change.url||change.status)sync();});
chrome.tabs.onRemoved.addListener(sync);
chrome.windows.onFocusChanged.addListener(sync);
chrome.storage.onChanged.addListener((changes)=>{if(['enabled','token','username','shareRoom'].some(k=>changes[k]))sync();});
chrome.runtime.onMessage.addListener(msg=>{if(msg?.type==='sync')sync();});
init();
