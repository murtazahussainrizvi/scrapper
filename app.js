document.getElementById("inputForm").addEventListener("submit", async function(event) {
    event.preventDefault();
  
    const url = document.getElementById("url").value;
    const className = document.getElementById("class").value;
    const nextPage = document.getElementById("nextpage").value;
  
    const data = {
      url: url,
      class: className,
      nextpage: nextPage
    };
  
    // Send POST request using Axios
    try {
      const response = await axios.post('http://127.0.0.1:5000/scrape', data, {
        responseType: 'arraybuffer' // Important: Set response type to arraybuffer for binary data
      });
  
      // Create a Blob from the response data
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  
      // Create a Blob URL and simulate a download link click
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = blobUrl;
      a.download = 'data.xls';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error('Error sending request:', error);
      // Handle errors here
    }
  });