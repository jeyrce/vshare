
window.onload=function(){
    setInterval("getTimes();", 1000);
}

function getTimes()
{
var oClock = document.getElementById("clock");

var aSpan = oClock.getElementsByTagName("span");
var aData = document.getElementById("Data");

    var oDate = new Date();
    var aDate = [oDate.getHours(), oDate.getMinutes(), oDate.getSeconds()];
    for (var i in aDate) {aSpan[i].innerHTML = format(aDate[i])}

    this.day = new Array("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六")[oDate.getDay()];

    aData.innerText=oDate.getFullYear()+"年"+(oDate.getMonth() + 1)+"月"+oDate.getDate()+"日 "+this.day+" ";
}
function format(a)
{
return a.toString().replace(/^(\d)$/, "0$1")

}






