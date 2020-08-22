# ClickbaitTime
ClickbaitTime is a Chrome/Firefox extension that allows you to find the timestamp in a YouTube video where its main thumbnail appears. If the thumbnail has been edited (eg. watermarked, logo added, etc) from the original frame, it will find the closest match.  

It will open the video at the timestamp in a new tab (no need to keep the extension open).

Note: We recommend using videos with durations under 15 minutes for good performance.  

![Demo](demo.gif)

## Setup
You can load the extension into your browser through the browser's extension tools page:

- Chrome/Opera:
  1. Type `chrome://extensions` in your address bar to bring up the extensions page.
  2. Enable developer mode (checkbox)
  3. Click the "Load unpacked extension" button, navigate to the `src/extension` folder of your local extension instance, and click "Ok".
- Firefox
  1. Type `about:debugging` in your address bar to bring up the add-ons page.
  2. Click the `Load Temporary Add-on` button, navigate to the `src/extension/manifest.json` file, and click "Open".

## Usage
Navigate to a YouTube video of your choice and click on the extension. In the popup that opens, click "Find Time". It might take a few seconds for the new tab to load; during this time, you can navigate away or close the extension.

## Credits
**Vincent Ji**: Implemented feature matching in OpenCV (Python) to find the best matching frame for the thumbnail in a given video.  
**Bowen Xu**: Developed front-end chrome extension (JavaScript) to retrieve video data and created a RESTful API (Python) that calls feature matching functionality on a Heroku server.
