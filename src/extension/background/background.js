let data={};
chrome.runtime.onMessage.addListener((request, sender, sendResponse)=>{
    data = {};
    console.log(request.value)
    let id = findId(request.value);
    data.id = id;
    let thumbnailURL = `https://i.ytimg.com/vi/${id}/mqdefault.jpg`;
    data.image = thumbnailURL;
    // fireLinksRequests(`https://youtubeaudio.majorcadevs.com/api/${id}/160`)
    Promise.then(()=>{
        return fireMessageRequest();
    }).then(jobId=>{
        console.log(jobId);
        return pollJob(jobId);
    }).then(timestampStr=>{
        console.log(timestampStr);
        let timestampLink = generateTimestampLink(timestampStr,id);        
        // chrome.runtime.sendMessage({type:'time', link: timestampLink, timestamp:timestampStr});
        chrome.tabs.create({"url": timestampLink});
        return;
    }).catch(error=>{
        console.error(error);
    });
    // console.log(thumbnailURL);

})

function generateTimestampLink(timestampStr,id){
    let parts = timestampStr.split(':');
    let totalTime = new Number(parts[0])*60 + new Number(parts[1]);
    return `https://youtu.be/${id}?t=${totalTime}`;
}


function findId(url){
    let index = url.indexOf('v=');
    let ampersandIndex = url.indexOf('&');
    let id;
    if (ampersandIndex === -1){
        id = url.substring(index+2);
    } else {
        id = url.substring(index+2, ampersandIndex);
    }
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
        let endpoint = `https://imagematcher.herokuapp.com/getmsg/?image=${data.image}&id=${data.id}`;     
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

function getTime(id){
    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
            let endpoint = `https://imagematcher.herokuapp.com/getTime/${id}`;     
            let xhr = new XMLHttpRequest();
            xhr.open("GET", endpoint); 
            xhr.onload = ()=>{
                if (xhr.status !== 200 && xhr.status !== 202) {
                    reject(xhr.statusText);
                } else {
                    resolve(xhr);
                }
            };
        xhr.send();
        }, 1000)
    })
}

async function pollJob(jobid){
    while(true){
        let xhr = await getTime(jobid);
        if (xhr.status === 200){
            let response = JSON.parse(xhr.response);
            return response.time;
        }
    }
}