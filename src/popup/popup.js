document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('button').addEventListener('click',retrieveUrl,false);
    chrome.runtime.onMessage.addListener((response,sender, sendResponse)=>{
        if (response.type === 'image'){
            document.querySelector('.image').textContent = `Thumbnail Link`;
            document.querySelector('.image').href = response.value;
        } else if (response.type === 'video'){
            document.querySelector('.video').textContent = `Video link`;
            document.querySelector('.video').href = response.value;
        } else {

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