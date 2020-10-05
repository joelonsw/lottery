var date = new Date();
var hour = date.getHours();
var min = date.getMinutes();
document.getElementById('time').min = `${hour}:${min}`
console.log(document.getElementById('time').min)


function submit_click(check) {
    //bool == true -> share
    //bool == false -> request
    console.log("!");
    var store = document.getElementById("store").value;
    var item = document.getElementById("item");
    //어떤 도넛인지
    var item_selected = item.options[item.selectedIndex].text;
    //몇개 요청했는지
    var number = document.getElementById("donut_number").value;
    //언제까지 띄울건지
    var time = document.getElementById("time").value;
    var sentense = "지점: "+store+ '\n' + "품목: " + item_selected + '\n' + "수량: "+number +'개\n' + time + ' 까지\n';
    if(check){
        sentense += 'Share 요청 하시겠습니까?';
    }else{
        sentense += 'Request 요청 하시겠습니까?';
    }
    
    if(confirm(sentense)){
        document.getElementById('submit_form').submit();
    }else{
        console.log("false");
        return false; 
    }
}