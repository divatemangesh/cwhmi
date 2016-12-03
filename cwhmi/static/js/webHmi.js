
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
//        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
//        if (numbers_received.length >= 10){
//            numbers_received.shift()
//        }
//        numbers_received.push(msg.number);
//        numbers_string = '';
//        for (var i = 0; i < numbers_received.length; i++){
//            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        trace3 = msg.number
//        }
//        $('#log').html(numbers_string);

//        var trace2 = {
//            x: [1, 2, 3, 4],
//            y: [16, 5, 11, 9],
//            type: 'scatter'
//            };
//
        var data = [trace3] //, trace2];
//
        Plotly.newPlot('plot', data);
        });

    socket.on('newImage', function(msg) {
        var dataUrlRgb="data:image/jpeg;base64,"+msg.imageRgb;
        document.getElementById("imageRgb").src = dataUrlRgb;
//        $('#log2').html(numbers_string);
        });

});
