chrome.runtime.onMessage.addListener((request, sender, sendResponse)=>{
    console.log(request.value)
    let id = findId(request.value);
    fireLinksRequests(`https://youtubeaudio.majorcadevs.com/api/${id}/160`);
    let thumbnailURL = `https://i.ytimg.com/vi/${id}/mqdefault.jpg`
    console.log(thumbnailURL);
    chrome.runtime.sendMessage({type:'image', value: thumbnailURL});
})

let oReq;

function findId(url){
    let index = url.indexOf('v=');
    let id = url.slice(index+2);
    return id;
}

function fireLinksRequests(endpoint){
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", endpoint); 
    oReq.send();
}

function reqListener(){
    if (oReq.status !== 200) {
        console.log('Failed request');
    } else {
        let response = JSON.parse(oReq.response);
        let videoURL = response.urls["160"];
        console.log(videoURL);
        chrome.runtime.sendMessage({type:'video', value:videoURL});
    }
}