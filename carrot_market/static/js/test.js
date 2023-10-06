document.addEventListener('DOMContentLoaded', function() {
    var writeForm = document.querySelector('.container');
    
    if (writeForm) {
        
        // Create a new WebSocket connection when the page is loaded.
        var socket = new WebSocket('ws://' + window.location.host + '/ai/');
        
        var autoButton = writeForm.querySelector('.auto');

        if (autoButton) {
            autoButton.addEventListener('click', function(event) {
                event.preventDefault();
                var postTitleElement = writeForm.querySelector('.id_post_title');
                var postTitle = postTitleElement ? postTitleElement.text : '';
                socket.send(JSON.stringify({question: postTitle}));
            });

            socket.onmessage = function(e) {
                var data = JSON.parse(e.data);
                var textContainer = document.querySelector(".text");
                textContainer.textContent += data.content;
                console.log(data.content);
            };
            
            socket.onclose= function(e){
              console.error('웹 소켓이 닫혔습니다');
           };
       }
   }
});