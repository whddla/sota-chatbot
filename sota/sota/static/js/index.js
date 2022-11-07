const banner = document.querySelector("div.banner");
    const arrows = document.querySelectorAll("div.arrow");
    const btns = document.querySelectorAll("button.btn");
    let count = 0;

    // 원하는 번호의 배너로 이동
    btns.forEach(function(btn, i, ar){
        // 각 버튼에 배너로 이동
        ar[i].addEventListener("click", function(){
            // 해당 버튼 번호(i)로 count 변경
            count = i;
            banner.style.transform = "translate(-" + count * 90 + "vw)";
        })
    })

    // 이전버튼, 다음버튼 기능 구현
    arrows.forEach(arrow => {
        arrow.addEventListener("click", function(){
            let arrowType = arrow.classList[1];
            if(arrowType == 'prev'){
                count--;
                if(count == -1) {
                    count = 5;
                }
            }else{
                count++;
                if(count == 6) {
                    count = 0;
                }
            }
            banner.style.transform = "translate(-" + count * 90 + "vw)";
        });
    });

    setInterval(function(){
        count++;
        count = count == 6 ? 0 : count;
        banner.style.transform = "translate(-" + count * 90 + "vw)";
    }, 2000);

