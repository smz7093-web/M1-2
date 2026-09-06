const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : 'https://m1-2-tyhj.onrender.com'; // 배포 후 본인의 Render URL로 수정

let currentConversationId = null;

// 1. 데이터 요약 불러오기
async function loadSummary() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/data/summary`);
    const data = await res.json();
    const card = document.getElementById('summary-card');
    card.innerHTML = `
      <strong>[현재 데이터 요약]</strong> 관측 기간: ${data.period} (총 ${data.total_count}건) | 
      최신 전국 빈집: <strong>${data.latest_total_value.toLocaleString()}호</strong> (10년 증가율: +${data.growth_10yr_pct}%)<br>
      비수도권 비중: <strong>${data.non_capital_share_pct}%</strong> | 상위 지역: ${data.top_regions.join(', ')}
    `;
  } catch (err) {
    document.getElementById('summary-card').innerText = "요약 정보를 불러오지 못했습니다. (서버 슬립 여부 확인)";
  }
}

// 2. 대화 목록 불러오기
async function loadConversations() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/conversations`);
    const list = await res.json();
    const ul = document.getElementById('conversation-list');
    ul.innerHTML = '';
    list.forEach(c => {
      const li = document.createElement('li');
      li.innerText = c.title;
      li.onclick = () => selectConversation(c.id);
      ul.appendChild(li);
    });
  } catch (err) {
    console.error("대화 목록 조회 실패", err);
  }
}

// 3. 특정 대화 불러오기 (불러오기 UX)
async function selectConversation(id) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/conversations/${id}`);
    const data = await res.json();
    currentConversationId = data.id;
    const container = document.getElementById('messages-container');
    container.innerHTML = '';
    data.messages.forEach(m => {
      appendMessage(m.role, m.content);
    });
  } catch (err) {
    alert("대화를 불러오는 중 오류가 발생했습니다.");
  }
}

function appendMessage(role, text) {
  const container = document.getElementById('messages-container');
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerText = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

// 4. 채팅 전송 (수정된 버전)
document.getElementById('chat-form').onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;

  appendMessage('user', msg);
  input.value = '';

  const spinner = document.getElementById('loading-spinner');
  spinner.classList.remove('hidden');

  try {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        conversation_id: currentConversationId, 
        message: msg 
      })
    });

    const data = await res.json();
    console.log("[백엔드 응답 원본 확인]:", data); // F12 개발자도구 콘솔에서 응답 구조 확인용

    if (!res.ok) {
      // 서버에서 4xx 또는 500 에러가 발생한 경우
      const errorMsg = data.detail || JSON.stringify(data);
      appendMessage('assistant', `⚠️ 서버 에러 발생: ${errorMsg}`);
      return;
    }

    currentConversationId = data.conversation_id;

    // 백엔드 응답을 문자열로 정규화해 undefined가 화면에 표시되지 않도록 처리
    const answer = typeof data === 'string'
      ? data
      : data.reply ?? data.response ?? data.answer ?? data.message ?? data.content;

    if (typeof answer === 'string' && answer.trim()) {
      appendMessage('assistant', answer);
    } else {
      appendMessage('assistant', `⚠️ 알 수 없는 응답 형식: ${JSON.stringify(data)}`);
    }

    loadConversations(); // 사이드바 목록 갱신
  } catch (err) {
    console.error("Fetch Error:", err);
    appendMessage('assistant', "⚠️ 네트워크 통신 중 오류가 발생했습니다. 백엔드 터미널을 확인하세요.");
  } finally {
    spinner.classList.add('hidden');
  }
};

// 5. 새 대화 시작 버튼
document.getElementById('btn-new-chat').onclick = () => {
  currentConversationId = null;
  const container = document.getElementById('messages-container');
  container.innerHTML = '<div class="msg assistant">새 대화를 시작합니다. 질문을 입력하세요!</div>';
};

// 6. 데이터 추가 (CRUD 동작)
document.getElementById('data-form').onsubmit = async (e) => {
  e.preventDefault();
  const date = document.getElementById('input-date').value;
  const value = parseFloat(document.getElementById('input-value').value);
  const memo = document.getElementById('input-memo').value;

  try {
    const res = await fetch(`${API_BASE_URL}/api/data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, value, memo })
    });
    if (res.ok) {
      document.getElementById('data-status').innerText = "데이터가 성공적으로 저장되었습니다!";
      document.getElementById('data-form').reset();
      loadSummary(); // 요약 통계 즉각 재계산
    }
  } catch (err) {
    document.getElementById('data-status').innerText = "저장 실패";
  }
};

// 초기 로딩
window.onload = () => {
  loadSummary();
  loadConversations();
};