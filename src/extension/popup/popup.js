document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('button').addEventListener('click',retrieveUrl,false);
    chrome.runtime.onMessage.addListener((response,sender, sendResponse)=>{
        if (response.type === 'time') {      
            document.querySelector('.time').textContent = response.timestamp;
            document.querySelector('.time').href=response.link;
        }
        return true;
    })
});

function retrieveUrl(){
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let url = tabs[0].url;
        sendMessage(url);
    });
};

function sendMessage(url){
    chrome.runtime.sendMessage({value:url});
}