document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('button').addEventListener('click',retrieveUrl,false);
});

function retrieveUrl(){
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let url = tabs[0].url;
        sendMessage(url);
    });
};

function sendMessage(url){
    chrome.runtime.sendMessage({value:url})
}