let data={};
chrome.runtime.onMessage.addListener((request, sender, sendResponse)=>{
    console.log(request.value)
    let id = findId(request.value);
    let thumbnailURL = `https://i.ytimg.com/vi/${id}/mqdefault.jpg`;
    data.image = thumbnailURL;
    fireLinksRequests(`https://youtubeaudio.majorcadevs.com/api/${id}/160`)
    .then(()=>{
        return fireMessageRequest();
    }).then(jobId=>{
        console.log(jobId);

    }).then(timestampStr=>{
        return;
    }).catch(error=>{
        console.error(error);
    });
    // console.log(thumbnailURL);
    // chrome.runtime.sendMessage({type:'image', value: thumbnailURL});

})


function findId(url){
    let index = url.indexOf('v=');
    let ampersandIndex = url.indexOf('&');
    let id = url.substring(index+2, ampersandIndex);
    return id;
}

function fireLinksRequests(endpoint){
    return new Promise((resolve,reject)=>{        
        let xhr = new XMLHttpRequest();
        xhr.open("GET", endpoint); 
        xhr.onload = ()=>{
            if (xhr.status !== 200) {
                reject(xhr.statusText);
            } else {
                let response = JSON.parse(xhr.response);
                let videoURL = response.urls["160"];
                console.log(videoURL);
                // chrome.runtime.sendMessage({type:'video', value:videoURL});
                videoURL = replaceAll(videoURL, '&', '%26');
                data.video = videoURL;
                resolve(xhr.response);
            }
        };
        xhr.send();
    });
}

function replaceAll(str, find, replace){
    return str.replace(new RegExp(find, 'g'), replace);
}

function fireMessageRequest(){
    return new Promise((resolve,reject)=>{   
        let endpoint = `https://imagematcher.herokuapp.com/getmsg/?image=${data.image}&video=${data.video}`;     
        let xhr = new XMLHttpRequest();
        xhr.open("GET", endpoint); 
        xhr.onload = ()=>{
            if (xhr.status !== 200) {
                reject(xhr.statusText);
            } else {
                let response = JSON.parse(xhr.response);
                let id = response.id;
                resolve(id);
            }
        };
        xhr.send();
    });
}

function reqListener(){
    
}