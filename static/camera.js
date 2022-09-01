function dataURLtoFile(dataurl, filename) {
 
    var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), 
        n = bstr.length, 
        u8arr = new Uint8Array(n);
        
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    
    return new File([u8arr], filename, {type:mime});
}



let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");

camera_button.addEventListener('click', async function() {
   	let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    $("#receipt-scan").css('display', 'block');
	video.srcObject = stream;
});

click_button.addEventListener('click', function() {
   	canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
   	let image_data_url = canvas.toDataURL('image/png');
    $("#receipt-image").attr('value', image_data_url);
});

$('#submit-receipt').click(function() {
    let image_data_url = $("#receipt-image").attr('value');
    console.log(image_data_url);
    let file = dataURLtoFile(image_data_url, 'receipt.png');
    let form_data = new FormData();
    form_data.append('receipt', file);
    $.ajax({
        url: '/scan-receipts',
        type: 'POST',
        data: form_data,
        contentType: false,
        processData: false,
        success: function(response) {
            console.log(response);
        }
    });
});