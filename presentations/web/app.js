
(function(){
  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));
  const status = (msg) => { $('#statusText').textContent = msg; };

  function sample3(arr){
    if(arr.length < 3) return arr.slice();
    const chosen = new Set();
    while(chosen.size < 3){
      chosen.add(Math.floor(Math.random()*arr.length));
    }
    return Array.from(chosen).map(i => arr[i]);
  }

  function renderCards(list){
    const wrap = $('#cards');
    wrap.innerHTML = '';
    list.forEach((q, idx) => {
      const card = document.createElement('article');
      card.className = 'card';
      card.setAttribute('aria-label', `שאלה ${idx+1}`);

      const imageBox = document.createElement('div');
      imageBox.className = 'image';

      const img = document.createElement('img');
      img.alt = '';
      img.src = `images/${q.slug}.png`;

      const emoji = document.createElement('span');
      emoji.className = 'emoji';
      emoji.textContent = q.emoji || '❓';

      img.addEventListener('error', () => {
        img.style.display = 'none';
        emoji.style.display = 'block';
      });

      imageBox.appendChild(img);
      imageBox.appendChild(emoji);

      const textBox = document.createElement('div');
      textBox.className = 'text';

      const cat = document.createElement('div');
      cat.className = 'category';
      cat.textContent = `[${q.category}]`;

      const question = document.createElement('div');
      question.className = 'question';
      question.textContent = q.question;

      textBox.appendChild(cat);
      textBox.appendChild(question);

      card.appendChild(imageBox);   // on the RIGHT (via row-reverse)
      card.appendChild(textBox);    // to the LEFT of image

      wrap.appendChild(card);
    });
  }

  function copyToClipboard(current, name){
    if(!current.length) return;
    const who = (name && name.trim()) ? name.trim() : 'ללא שם';
    const lines = [`ל' ${who} – 3 שאלות:\n`];
    current.forEach((q, i) => lines.push(`${i+1}. [${q.category}] ${q.question}`));
    const text = lines.join('\n');
    navigator.clipboard.writeText(text).then(
      () => status('הטקסט הועתק ללוח.'),
      () => status('שגיאה בהעתקה ללוח.')
    );
  }

  function logAssignment(current, name){
    try {
      const logs = JSON.parse(localStorage.getItem('assignment_logs') || '[]');
      logs.push({
        ts: new Date().toISOString(),
        student: name || '',
        questions: current.map(q => ({id:q.id, category:q.category, question:q.question}))
      });
      localStorage.setItem('assignment_logs', JSON.stringify(logs));
    } catch(e){ /* ignore */ }
  }

  let current = [];

  document.addEventListener('DOMContentLoaded', () => {
    const nameInput = $('#studentName');
    $('#btnGenerate').addEventListener('click', () => {
      current = sample3(window.QUESTIONS || []);
      renderCards(current);
      logAssignment(current, nameInput.value);
      status('הוגרלו 3 שאלות חדשות.');
    });
    $('#btnCopy').addEventListener('click', () => copyToClipboard(current, nameInput.value));
    $('#btnNext').addEventListener('click', () => {
      nameInput.value = '';
      current = [];
      $('#cards').innerHTML = '';
      status('מוכן לתלמיד/ה הבא/ה.');
      nameInput.focus();
    });
  });
})();
