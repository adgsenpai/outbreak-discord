const $=id=>document.getElementById(id);
async function render(){
 const s=await chrome.storage.local.get(['enabled','token','username','shareRoom','connected','playing','game','room','lastError']);
 $('enabled').checked=s.enabled!==false;
 if(document.activeElement!==$('token'))$('token').value=s.token||'';
 if(document.activeElement!==$('username'))$('username').value=s.username||'';
 $('shareRoom').checked=s.shareRoom===true;
 $('status').textContent=s.connected?(s.playing?`🟢 ${s.game||'Outbreak'} active${s.room?' · '+s.room.name+' ('+(s.room.players||'?')+')':''}`:'🟢 Connected — focus an Outbreak tab'):`🔴 Disconnected${s.lastError?': '+s.lastError:''}`;
}
$('save').addEventListener('click',async()=>{
 await chrome.storage.local.set({token:$('token').value.trim(),username:$('username').value.trim(),enabled:$('enabled').checked,shareRoom:$('shareRoom').checked});
 chrome.runtime.sendMessage({type:'sync'}).catch(()=>{});setTimeout(render,600);
});
$('enabled').addEventListener('change',async()=>{await chrome.storage.local.set({enabled:$('enabled').checked});setTimeout(render,600);});
render();
