function handleSubmit(){
    const message = document.getElementById('message');

    var audio = new Audio('/static/cashsound.mp3');
    audio.play();

    message.innerHTML='Counting the Cash Please wait....';

    setTimeout(function(){message.innerHTML='Deposited Successfully'}, 5000);
}