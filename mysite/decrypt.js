

// function decrypt(){

	var blob = null;
	var xhr = new XMLHttpRequest(); 
	xhr.open("GET", "http://127.0.0.1:8000/media/glass6/home/anurag/Data/Sample.txt"); 
	// xhr.responseType = "blob";//force the HTTP response, response-type header to be blob
	// alert("hoolahoo");
	xhr.onload = function() 
	{

	    var text = xhr.response;//xhr.response is now a blob object
	    blob = text;
	    console.log("arggrg");
	}
	xhr.send();
	str = "newhoolahoo";

	var blobUrl = URL.createObjectURL(blob);
	var link = document.createElement("a"); // Or maybe get it from the current document
link.href = blobUrl;
link.download = "aDefaultFileName.txt";
link.innerHTML = "Click here to download the file";
document.body.appendChild(link);
	// var reader = new FileReader();
	// reader.onload = function() {
	//     alert(reader.result);
	// }
	// reader.readAsText(blob);
	// // var myReader = new FileReader();
	// myReader.addEventListener("loadend", function(e){
	//     var str = e.srcElement.result;
	// });
	// // alert(str);
	// myReader.readAsText(blob);
	// document.getElementbyId("demo").innerHTML = str;
	// alert(str);
// }
requestUrl = "http://127.0.0.1:8000/media/glass6/home/anurag/Data/Sample.txt";
// var xhr = new XMLHttpRequest;
// xhr.open("GET", requestUrl);
// xhr.addEventListener("load", function () {
//     var ret = [];
//     var len = this.responseText.length;
//     var byte;
//     for (var i = 0; i < len; i++) {
//         byte = (this.responseText.charCodeAt(i) & 0xFF) >>> 0;
//         ret.push(String.fromCharCode(byte));
//     }
//     var data = ret.join('');
//     data = "data:application/pdf;base64," + btoa(data);

//     window.open(data, '_blank', 'resizable, width=1020,height=600');
// }, false);

// xhr.setRequestHeader("Authorization", "Bearer " + client.accessToken);
// xhr.overrideMimeType("octet-stream; charset=x-user-defined;");
// xhr.send(null);
// var xhr = new XMLHttpRequest();
// xhr.open("GET", requestUrl);
// xhr.responseType = "blob";

// xhr.onload = function () {
//     onDownloaded(this);
// };
// xhr.send(null);

// axios.get(requestUrl, {
//       responseType: 'arraybuffer',
//       headers: {
//         'Accept': 'application/pdf'
//       }
// }).then(response => {
// 	console.log(response.data);
//     const blob = new Blob([response.data], {
//       type: 'application/pdf',
//     });
//     FileSaver.saveAs(blob, 'file.pdf');
// });