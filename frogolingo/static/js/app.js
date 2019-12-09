
const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    var audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data)
    });

    const start = () => {
                audioChunks = []
                mediaRecorder.start()
                };

const stop = () =>
  new Promise(resolve => {
    mediaRecorder.addEventListener("stop", () => {
      let audioDownload = document.createElement("a");
      const audioBlob = new Blob(audioChunks,{type:'audio/x-mpeg-3'});
      audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      const play = () => audio.play();
      resolve({ audioBlob, audioUrl, play, audioDownload});

      audioDownload.href = audioUrl;
      audioDownload.download = 'mp3';
      audioDownload.innerHTML = 'download';
      document.body.appendChild(audioDownload);

    });

    mediaRecorder.stop();

  });


    resolve({ start, stop });
  });


$(function() {
    var recordedAudio;
      recordAudio().then((recorder)=>{
        $('#recording').on("click", function(event){
        event.preventDefault();
        console.log("kliknięty!")
        if (event.target.value == "Start recording..."){
            recorder.start()
            event.target.value = "Stop recording..."
            $('#play').addClass("hidden");
            }
        else if(event.target.value == "Stop recording..."){
            recorder.stop().then((audio)=> recordedAudio = audio)
            event.target.value = "Start recording..."
                $('#play').removeClass("hidden")
                $('#download').removeClass("hidden")
            }
        })
        $('#play').on('click', function(event){
            event.preventDefault();
            recordedAudio.play()
        })

         $('#audioDownload').on('click', function(event){
            event.preventDefault();
            })
        })
})