// 간단한 WebSocket 기반 시뮬레이션 클라이언트
(function () {
    const input = document.getElementById("thoughtInput");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");
    const resultArea = document.getElementById("resultArea");

    let ws = null;
    function connect() {
        const protocol = location.protocol === "https:" ? "wss" : "ws";
        const url = `${protocol}://${location.host}/ws/sim`;
        ws = new WebSocket(url);
        ws.onopen = () => {
            console.log("WebSocket connected");
        };
        ws.onmessage = (evt) => {
            try {
                const data = JSON.parse(evt.data);
                resultArea.textContent = JSON.stringify(data, null, 2);
            } catch (e) {
                resultArea.textContent = evt.data;
            }
        };
        ws.onclose = () => {
            console.log("WebSocket closed, reconnect in 1s");
            setTimeout(connect, 1000);
        };
        ws.onerror = (err) => {
            console.error("WebSocket error", err);
            ws.close();
        };
    }

    sendBtn.addEventListener("click", () => {
        const text = input.value.trim();
        if (!text) return alert("생각을 입력하세요.");
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            // 연결이 없으면 새로 연결 후 전송
            connect();
            // 잠깐 대기 후 전송 (간단 구현)
            setTimeout(() => {
                if (ws && ws.readyState === WebSocket.OPEN) ws.send(text);
                else alert("서버에 연결할 수 없습니다. 잠시 후 다시 시도하세요.");
            }, 300);
        } else {
            ws.send(text);
        }
    });

    clearBtn.addEventListener("click", () => {
        input.value = "";
        resultArea.textContent = "{아직 없음}";
    });

    // 페이지 로드 시 연결 시도
    connect();
})();
