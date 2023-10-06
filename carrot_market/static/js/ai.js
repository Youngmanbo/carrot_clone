document
    .querySelector("#ai-container")
    .addEventListener('click', function(){
        let main = document.querySelector('.chat-container');
        main.innerHTML = ''
        html = `<div class='message-box assistant'>
                <div class="message-text">안녕하세요 쉐이크캐럿 봇입니다.</div></div>`
        main.innerHTML += html

        const aiSocket = new WebSocket('ws://' + window.location.host + '/ws/ai/');

        //메세지 실시간으로 채팅창에 넣음
        aiSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            
            
            // 메시지의 발신자가 현재 사용자인지 확인
            const isFromMe = null;
            
            // 메시지 박스의 CSS 클래스를 설정
            const messageClass = isFromMe ? "from-me" : "";
            
            // 메시지 박스를 동적으로 생성하고 페이지에 추가
            let chatLogTest = document.getElementById("chat-log");
            chatLogTest.innerHTML += `<div class="message-box ${messageClass}">
                <div class="message-text">${data.message}</div>
              </div>`;
          };
          aiSocket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
          };
        // 채팅창에 키 들어가있도록 함
        document
          .querySelector('#chat-message-input')
          .focus();

        // 채팅 전송
        document
          .querySelector('#chat-message-input')
          .onkeyup = function (e) {
            if (e.keyCode === 13) { // enter, return
              document
                .querySelector('#chat-message-submit')
                .click();
            }
          };
        
        
        let chatBtn = document.querySelector("#chat-message-submit");

        var aiclick = function(e){
            e.preventDefault();
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            console.log(message);
            aiSocket.send(JSON.stringify({question: message}));
            messageInputDom.value = ''
        }

        chatBtn.removeEventListener('click', messageSend);
        chatBtn.addEventListener('click', aiclick);
    })