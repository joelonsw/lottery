var date = new Date();
var hour = date.getHours();
var min = date.getMinutes();
document.getElementById('time').min = `${hour}:${min}`
// console.log(document.getElementById('time').min)

function submit_click(check) {
    var store = document.getElementById("store").value;
    //어떤 도넛인지
    //몇개 요청했는지
    var number = document.getElementById("number").value;
    //언제까지 띄울건지
    var time = document.getElementById("time").value;
    var sentense = "지점: "+store+ '\n' + "수량: "+number +'개\n' + time + ' 까지\n';
    //check == true -> 제가 가져갈게요
    if(check){
        sentense += '가져가시겠어요?';
    }else{
        sentense += '도와주시겠어요?';
    }
    console.log(sentense);
    if(confirm(sentense)){
        document.getElementById('submit_form').submit();
    }else{
        console.log("false");
        return false; 
    }
}