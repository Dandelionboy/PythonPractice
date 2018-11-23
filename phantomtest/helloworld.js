var  paage=require('webpage').create()
phantom.outputEncoding="gbk"
paage.open('http://www.cnblogs.com/front-Thinking',function (statuc) {
    if (statuc==="success"){
        console.log(paage.title)
    }else {
        console.log("not find")
    }
    phantom.exit()
});