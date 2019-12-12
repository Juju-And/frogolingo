
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
      let audioDownload = $('#audioDownload')
      const audioBlob = new Blob(audioChunks,{type:'audio/x-mpeg-3'});
      audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      const play = () => audio.play();
      resolve({ audioBlob, audioUrl, play, audioDownload});

//      var file = new File([audioBlob], audioUrl+'.mp3')
      audioDownload.href = audioUrl;
      audioDownload.download = '/' + audioUrl + '.mp3';
//      audioDownload.innerHTML = 'download';
      audioDownload.removeClass("hidden")
//      document.body.appendChild(audioDownload);

    });

    mediaRecorder.stop();

  });


    resolve({ start, stop });
  });


function saveAnswer(answer, expression_id) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    console.log("create post is working!") // sanity check
//    console.log($('#product-name').val())
        $.ajax({
            url: "http://127.0.0.1:8000/training/",
            data: JSON.stringify({'answer': answer,
            'expression_id': expression_id}),
            headers:{
            "X-CSRFToken": csrftoken
            },
            type: "POST",
            dataType: "json"
        }).done(function(response) {
            console.log('odpowiedź przesłana')
        }).fail(function(xhr,status,err) {
        }).always(function(xhr,status) {
        });
}



$(function() {
    console.log('dupa')
    let a =  $('#audioDownload')
    console.log(a)

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
//                $('#audioDownload').removeClass("hidden")

            }
        })
        $('#play').on('click', function(event){
            event.preventDefault();
            recordedAudio.play()
        })

//         $('#audioDownload').on('click', function(event){
//            event.preventDefault();
//            })

    })

        $('#show_pic').click(function(){
            console.log("kliknięty!")
            $('#show_pic').addClass("hidden")
            $('#hint').removeClass("hidden")
        })

        $('#submit_answer').on('click', function(event){
            event.preventDefault();
            let answer
            let expression_id
            if ($('#reference').attr('data-translation') == $('#answer').val()) {
                expression_id = $('#reference').attr('data-id')
                answer = true
                $('.correct_hide').addClass("hidden")
                $('.correct_show').removeClass("hidden")
                $('#answer').removeClass("error-field")
                $('#answer').addClass("correct-field")

//                console.log('odpowiedź prawidłowa!')
            } else {
                answer = false
                expression_id = $('#reference').attr('data-id')
//                console.log('odpowiedź nieprawidłowa!')
                $('#answer').addClass("error-field")
            }
            saveAnswer(answer, expression_id);
        })


})