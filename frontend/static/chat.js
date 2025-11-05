const $ = sel => document.querySelector(sel);
const historyEl = $('#history');
const promptEl  = $('#prompt');
const sendBtn   = $('#send');

function addMsg(role, text){
  const row = document.createElement('div');
  row.className = `msg ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  row.appendChild(bubble);
  historyEl.appendChild(row);
  historyEl.scrollTop = historyEl.scrollHeight;
}

async function run(){
  const prompt = (promptEl.value || '').trim();
  if(!prompt) return;
  addMsg('user', prompt);
  promptEl.value = '';

  const loading = document.createElement('div');
  loading.className = 'msg bot';
  const b = document.createElement('div');
  b.className = 'bubble';
  b.textContent = 'Thinking…';
  loading.appendChild(b);
  historyEl.appendChild(loading);
  historyEl.scrollTop = historyEl.scrollHeight;

  try{
    const r = await fetch('http://127.0.0.1:8080/api/run', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({prompt})
    });
    const data = await r.json();
    loading.remove();
    if(data.response){
      addMsg('bot', data.response);
    }else{
      addMsg('bot', `Error: ${data.error || 'Unknown error'}`);
    }
  }catch(e){
    loading.remove();
    addMsg('bot', `Network error: ${e.message}`);
  }
}

sendBtn?.addEventListener('click', run);
promptEl?.addEventListener('keydown', e => {
  if(e.key === 'Enter') run();
});
