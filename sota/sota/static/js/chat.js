$(function(){

    // SEND 버튼을 누르거나
    $("#sendbtn").click(function(){
        send_message();
    });

    // ENTER key 가 눌리면
    $("#chattext").keyup(function(event){
        if(event.keyCode == 13){
            send_message();
        }
    });

});

function send_message(){
    const chattext = $("#chattext").val().trim();

    // 입력한 메세지가 없으면 리턴
    if(chattext == ""){
        $("#chattext").focus();
        return;
    }

    // 입력한 채팅 출력

    addtext = "<div class=customer><div class=customer-wrap><div class=txt><div>"+chattext+"</div></div><div class=time><div>오후5:15</div></div></div></div>";
    $("#chatbox").append(addtext);    

    // API 서버에 보낼 데이터 준비
    const jsonData = {
        query: chattext,
        bottype: "WebClient",
    };
    console.log(jsonData)
    $.ajax({
        url: 'http://127.0.0.1:5000/chatbot/TEST',
        type: "POST",
        data: JSON.stringify(jsonData),
        dataType: "JSON",  // 응답받을 데이터 타입
        contentType: "application/json; charset=utf-8",  
        crossDomain: true,
        success: function(response){
            console.log(response)
            // response.Answer 에 챗봇의 응답메세지가 담겨 있다
            $chatbox = $("#chatbox");
            // 답변 출력

            bottext ="<div class=chat-bot><div class=bot-profile><div class=img style=background: none;><img src=https://openclipart.org/image/800px/262355 alt=챗봇></div><div class=name>챗봇</div></div><div class=bot-talk><div class=txt><div>"+response.Answer+"</div></div><div class=time><div>오후5:10</div></div></div></div>";
            $chatbox.append(bottext);
            if(response.Intent=='인사'){

            }
            // 스크롤 조정하기
            $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')});

            // 먼저 입력했던 내용은 지우기
            $("#chattext").val("");
            $("#chattext").focus();
        },
    });
} // end 