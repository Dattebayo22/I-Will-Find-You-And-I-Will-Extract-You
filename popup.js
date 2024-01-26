document.addEventListener('DOMContentLoaded', function () {
    var saveButton = document.getElementById('saveButton');

    saveButton.addEventListener('click', function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var currentUrl = tabs[0].url;
            alert(currentUrl);
            const page_number = prompt('Enter the page number:');
            
            if (page_number !== null) {
                const extractedPart = extractPartFromUrl(currentUrl);

                if (extractedPart) {
                    fetch(`http://localhost:5000/get/${extractedPart}/${page_number}`)
                    .then(response => response.text())
                    .then(result => {
                    alert(result);
      })
      .catch(error => console.error('Error:', error));

                } else {
                    alert("No match found in the URL");
                }
            } else {
                alert("User canceled the operation.");
            }
        });
    });
    function extractPartFromUrl(url) {
        const pattern = /\/books\/edition\/[^/]+\/([^?]+)\?/;
        const match = url.match(pattern);

        return match ? match[1] : null;
    }
    function saveToFile(content, page_number) {
        const textContent = `${content}\n${page_number}`;

        chrome.downloads.download({
            url: 'data:text/plain;charset=utf-8,' + encodeURIComponent(textContent),
            filename: 'extracted_url.txt',
            saveAs: true
        }, function (downloadId) {
            if (chrome.runtime.lastError) {
                console.error('Download error: ' + chrome.runtime.lastError.message);
                alert('Error saving file. Please try again.');
            } else {
                console.log('Download started with ID: ' + downloadId);
                alert('Data saved to file: extracted_url.txt');
            }
        });
    }
});