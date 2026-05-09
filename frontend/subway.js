let logs = JSON.parse(localStorage.getItem('subway_logs')) || [];

// 8일차 삭제 로직 (현재 시간 기준 8일 전 데이터는 모두 삭제)
function deleteOldLogs() {
    const limitTime = Date.now() - (8 * 86400000); 
    const initialCount = logs.length;
    logs = logs.filter(log => new Date(log.time).getTime() > limitTime);
    
    if (initialCount !== logs.length) {
        localStorage.setItem('subway_logs', JSON.stringify(logs));
    }
}

// 테스트 데이터 생성
function createTestData(daysAgo) {
    const types = ['무단 통과', '다인 통과', '게이트 월담'];
    const randomType = types[Math.floor(Math.random() * types.length)];
    
    // 정확히 n일 전 같은 시간대로 설정
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() - daysAgo);

    const newLog = {
        id: Date.now() + Math.random(),
        time: targetDate.toISOString(),
        type: `[테스트] ${randomType}`,
        img: `https://via.placeholder.com/600x400/333333/ffffff?text=${daysAgo}DaysAgo`
    };

    logs.unshift(newLog);
    localStorage.setItem('subway_logs', JSON.stringify(logs));
    alert(`${daysAgo}일 전 데이터가 생성되었습니다.`);
    if (document.getElementById('viewHistory').classList.contains('active')) renderLogs();
}

function renderLogs() {
    deleteOldLogs(); 
    const container = document.getElementById('historyGroupsContainer');
    if (!container) return;
    container.innerHTML = '';
    
    if (logs.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding:50px; color:#666;">기록이 없습니다.</div>';
        return;
    }

    logs.sort((a, b) => new Date(b.time) - new Date(a.time));
    const grouped = {};
    
    logs.forEach(log => {
        const logDate = new Date(log.time);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const compareDate = new Date(logDate);
        compareDate.setHours(0, 0, 0, 0);
        const diffDays = Math.floor((today - compareDate) / 86400000);
        
        let label = diffDays === 0 ? "오늘" : (diffDays === 1 ? "1일 전" : `${diffDays}일 전`);
        if (!grouped[label]) grouped[label] = [];
        
        // 7일차인지 체크 (8일차에 삭제되므로 7일차가 마지막 날임)
        log.isExpiring = (diffDays === 7);
        grouped[label].push(log);
    });

    for (const [dateLabel, items] of Object.entries(grouped)) {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'date-group';
        groupDiv.innerHTML = `
            <div class="date-header" style="color:${items[0].isExpiring ? 'var(--expiring-color)' : 'var(--danger-color)'}">${dateLabel}</div>
            <div class="history-grid">
                ${items.map(item => `
                    <div class="history-card ${item.isExpiring ? 'expiring' : ''}" onclick="viewDetail(${item.id})">
                        ${item.isExpiring ? `<div class="expiring-label">곧 데이터가 사라집니다.</div>` : ''}
                        <img src="${item.img}" alt="Capture">
                        <div class="card-body">
                            <div style="font-size:0.7rem; color:#888;">${new Date(item.time).toLocaleString()}</div>
                            <div style="color:${item.isExpiring ? 'var(--expiring-color)' : 'var(--danger-color)'}; font-weight:bold; font-size:0.85rem;">${item.type}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(groupDiv);
    }
}

// 기존 인터페이스 함수들
function switchView(viewName) {
    document.querySelectorAll('.view-content').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    const target = document.getElementById(`view${viewName.charAt(0).toUpperCase() + viewName.slice(1)}`);
    if (target) target.classList.add('active');
    
    if (viewName === 'history') {
        renderLogs();
        document.querySelectorAll('.tab-button')[1].classList.add('active');
    } else if (viewName === 'main') {
        document.querySelectorAll('.tab-button')[0].classList.add('active');
    }
}

function simulateDetection() {
    const types = ['무단 통과', '다인 통과', '게이트 월담'];
    const randomType = types[Math.floor(Math.random() * types.length)];
    const modal = document.getElementById('alertModal');
    const overlay = document.getElementById('modalOverlay');
    
    document.getElementById('alertDetails').innerHTML = `<h2 style="margin:0; color:var(--danger-color)">${randomType}</h2><p style="color:#ccc">즉시 확인하십시오.</p>`;
    modal.style.display = 'block';
    overlay.style.display = 'block';

    logs.unshift({
        id: Date.now(),
        time: new Date().toISOString(),
        type: randomType,
        img: `https://via.placeholder.com/600x400/ff4d4d/ffffff?text=DETECTED`
    });
    localStorage.setItem('subway_logs', JSON.stringify(logs));
}

function closeAlert() {
    document.getElementById('alertModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
    switchView('history');
}

function viewDetail(id) {
    const log = logs.find(item => item.id === id);
    if (!log) return;
    document.getElementById('detailImage').src = log.img;
    document.getElementById('detailType').innerText = log.type;
    document.getElementById('detailTime').innerText = new Date(log.time).toLocaleString();
    switchView('detail');
}


function resetAllData() {
    // 사용자에게 한 번 더 확인
    const confirmReset = confirm("모든 감지 기록이 영구적으로 삭제됩니다. 계속하시겠습니까?");
    
    if (confirmReset) {
        // 1. 메모리 상의 로그 배열 비우기
        logs = [];
        
        // 2. 로컬 스토리지 데이터 삭제
        localStorage.removeItem('subway_logs');
        
        // 3. UI 업데이트
        // 만약 기록 탭에 있다면 즉시 빈 화면 렌더링
        if (document.getElementById('viewHistory').classList.contains('active')) {
            renderLogs();
        }
        
        alert("모든 기록이 초기화되었습니다.");
    }
}

document.addEventListener('DOMContentLoaded', renderLogs);