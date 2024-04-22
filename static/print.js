function handlePrint(){
    const message = document.getElementById('message');

    var audio = new Audio('/static/cashsound.mp3');
    audio.play();

    message.innerHTML='Printing......';

    setTimeout(function(){message.innerHTML='Please collect the receipt'}, 5000);
}