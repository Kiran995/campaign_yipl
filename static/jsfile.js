$(document).ready(function () {

var $remaining = $('#charNum'),
    $messages = $remaining.prev();
    $maxVal = 160;

$('.word-counter').keyup(function(){
    var chars = this.value.length,
        messages = Math.ceil(chars / $maxVal),
        remaining = messages * $maxVal - (chars % (messages * $maxVal) || messages * $maxVal);

    $remaining.text(remaining + ' characters remaining');
    $messages.text(messages + ' message(s) / ');
});




});