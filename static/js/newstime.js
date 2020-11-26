function countDown(time) {
    var nowTime = +new Date(); //返回的是房钱时间的总的毫秒数
    var inputTime = +new Date(time); // 返回的是用户输入的时间总的毫秒数
    var times = (nowTime - inputTime) / 1000; //times是 剩余时间的总的秒数

    var d = parseInt(times / 60 / 60 / 24); // 天
    // d = d < 10 ? '0' + d : d;
    if (d == '0') {
        d = '';
    } else {
        d += '일';
    }

    var h = parseInt(times / 60 / 60 % 24); // 时
    // h = h < 10 ? '0' + h : h;
    if (h == '0') {
        h = '';
    } else {
        h += '시간';
    }
    var m = parseInt(times / 60 % 60); //分
    // m = m < 10 ? '0' + m : m;
    if (m == '0') {
        m = '';
    } else {
        m += '분';
    }
    var s = parseInt(times % 60); //当前的秒
    // s = s < 10 ? '0' + s : s;
    if (s == '0') {
        s = '';
    } else {
        s += '초';
    }
    if (h != 0) {
        return d + h + ' 전';
    } else {
        return d + h + m + ' 전';
    }

    }
var newsTime = document.querySelectorAll('#newstimes');
for(i in newsTime) {
    newsTime[i].innerText = countDown(newsTime[i].innerText);
}

