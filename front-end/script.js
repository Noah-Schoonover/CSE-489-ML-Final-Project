var ctx, color = "#000";

$(document).ready(function () {

  // setup a new canvas for drawing wait for device init
    setTimeout(function(){
     newCanvas();
    }, 1000);

  // link the new button with newCanvas() function
  $("#new").click(function() {
    newCanvas();
  });
});

// function to setup a new canvas for drawing
function newCanvas(){

    var canvas = '<canvas id="canvas" width="400px" height="400px"></canvas>';
  $("#canvasDiv").html(canvas);
    var can=document.getElementById("canvas");

    // setup canvas
  ctx=can.getContext("2d");

    ctx.strokeStyle = "#FF0000";
    ctx.beginPath();
    //ctx.rect(100, 55, 200, 285);
    ctx.stroke();

  ctx.strokeStyle = color;
  ctx.lineWidth = 35;
    ctx.lineCap = 'round';

  // setup to trigger drawing on mouse or touch
   $("#canvas").drawTouch();
    // $("#canvas").drawPointer();

    $("#result").text("")

    var lastEvent;
    var mouseDown;

    //On mouse events on the canvas:
    $("#canvas").mousedown(function(e) {
      //On mousedown, storing the starting coordinates and enable the drawing.
      lastEvent = e; //saving the starting coordinates
      mouseDown = true; //drawing enabled
    }).mousemove(function(e) {
      //On mousemove draws the path, change the style, stroke the line, update the coordinates.
      if (mouseDown) {
        ctx.beginPath(); //begin the path
        ctx.moveTo(lastEvent.offsetX, lastEvent.offsetY); //starting coordinates
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke(); //draw the path
        lastEvent = e; //replacing the coordinates
      }
    }).mouseup(function() {
        //On mouseup drawing disabled
        mouseDown = false;

        resizeTo(can, 28);

        //testSocket();

    }).mouseleave(function(){

      if(mouseDown) {
          $("#canvas").mouseup();
      }

    });
}

function resizeTo(canvas, size){
    // size is used for width and height for square images

    var cw=canvas.width;
    var ch=canvas.height;
    var ctx=canvas.getContext('2d');

////////////////////////////////////////////////////////////////////
var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height),
  data = imageData.data,
  getRBG = function(x, y) {
    var r = data[(canvas.width*y + x) * 4],
      g = data[(canvas.width*y + x) * 4 + 1],
      b = data[(canvas.width*y + x) * 4 + 3];

    if (r != 0) { b = 0; }

    return {
      red: r,
      green: g,
      blue: b
    };
  },
  isWhite = function (rgb) {
        return rgb.blue == 0;
      },
  scanY = function (fromTop) {
        var offset = fromTop ? 1 : -1;

        // loop through each row
        for(var y = fromTop ? 0 : canvas.height - 1; fromTop ? (y < canvas.height) : (y > -1); y += offset) {

        // loop through each column
        for(var x = 0; x < canvas.width; x++) {
          if (!isWhite(getRBG(x, y))) {
            return y;
          }
        }
      }
      return null; // all image is white
    },
  scanX = function (fromLeft) {
        var offset = fromLeft? 1 : -1;

        // loop through each column
        for(var x = fromLeft ? 0 : canvas.width - 1; fromLeft ? (x < canvas.width) : (x > -1); x += offset) {

        // loop through each row
        for(var y = 0; y < canvas.height; y++) {
          if (!isWhite(getRBG(x, y))) {
            return x;
          }
        }
      }
      return null; // all image is white
    };


var cropTop = scanY(true),
  cropBottom = scanY(false),
  cropLeft = scanX(true),
  cropRight = scanX(false);
  cropWidth = cropRight - cropLeft,
  cropHeight = cropBottom - cropTop;
  //console.log(cropTop, cropBottom, cropLeft, cropRight);
  //console.log(cropWidth, cropHeight);

var $croppedCanvas = $("<canvas>").attr({ width: cropWidth, height: cropHeight, id: 'debugCanvas' });

// finally crop the guy
$croppedCanvas[0].getContext("2d").drawImage(canvas,
  cropLeft, cropTop, cropWidth, cropHeight,
  0, 0, cropWidth, cropHeight);

$("[id=debugCanvas]").remove();
$("body").
  append("<p id='debugCanvas'>cropped canvas:</p>").
  append($croppedCanvas);
// cropTop is the last topmost white row. Above this row all is white
// cropBottom is the last bottommost white row. Below this row all is white
// cropLeft is the last leftmost white column.
// cropRight is the last rightmost white column.

//////////////////////////////////////////////////////////////////

var centeredCanvas=document.createElement("canvas");
    var cctx=centeredCanvas.getContext("2d")
    centeredCanvas.width=canvas.width;
    centeredCanvas.height=canvas.height;
centeredCanvas.id = 'debugCanvas'

//100, 55, 200, 285
var targetWidth = 100;
var targetHeight = 230;
var scale = 1;

if ($croppedCanvas[0].width > $croppedCanvas[0].height) {
  scale = targetWidth / $croppedCanvas[0].width;
  //console.log("scaling with respect to width");
} else {
  scale = targetHeight / $croppedCanvas[0].height;
  //console.log("scaling with respect to height");
}

var newWidth = $croppedCanvas[0].width*scale;
var newHeight = $croppedCanvas[0].height*scale;

cctx.drawImage($croppedCanvas[0],
    centeredCanvas.width/2 - newWidth/2,
    centeredCanvas.height/2 - newHeight/2,
    newWidth,
    newHeight);

$("body").
  append("<p  id='debugCanvas'>centered canvas:</p>").
  append(centeredCanvas);

var tempCanvas=document.createElement("canvas");
    var tctx=tempCanvas.getContext("2d")
    tempCanvas.width=size;
    tempCanvas.height=size;
tctx.drawImage(centeredCanvas,0,0,size,size);
    var img = new Image();
    img.src = tempCanvas.toDataURL();
    $("img").remove();
    $("#canvasDiv").append(img);
    imgData = tctx.getImageData(0,0,tempCanvas.width,tempCanvas.height);

    gsData = new Array(imgData.data.length / 4);
    console.log("gsData length: " + gsData.length);

    for(i = 0; i < imgData.data.length; i += 4) {
        if (imgData.data[i+3]) {
    gsData[i/4] = 0;
  }
        gsData[i/4] = imgData.data[i+3];
    }

console.log("image data: " + gsData);


    // Create WebSocket connection.
    // const socket = new WebSocket('ws://127.0.0.1:8765');
const socket = new WebSocket('ws://128.199.4.66:8765');

    socket.onopen = function() {
        socket.send(JSON.stringify(gsData));
    };

    socket.onmessage = function(s) {
        $("#result").text(s.data)
    };
}


// prototype to	start drawing on touch using canvas moveTo and lineTo
$.fn.drawTouch = function() {
  var start = function(e) {
    e = e.originalEvent;
    ctx.beginPath();
    var touch = e.changedTouches[0];
    x = touch.pageX-touch.target.offsetLeft;
    y = touch.pageY-touch.target.offsetTop;
    ctx.moveTo(x,y);
  };
  var move = function(e) {
    e.preventDefault();
    e = e.originalEvent;
    var touch = e.changedTouches[0];
    x = touch.pageX-touch.target.offsetLeft;
    y = touch.pageY-touch.target.offsetTop;
    console.log("move   x: " + x + "     y: " + y);
    ctx.lineTo(x,y);
    ctx.stroke();
  };
  var finish = function(e) {
    var can=document.getElementById("canvas");
    resizeTo(can, 28);
  };
  $(this).on("touchstart", start);
  $(this).on("touchmove", move);
  $(this).on("touchend", finish);
  $(this).on("touchcancel", finish);
};

// prototype to	start drawing on pointer(microsoft ie) using canvas moveTo and lineTo
$.fn.drawPointer = function() {
  var start = function(e) {
        e = e.originalEvent;
    ctx.beginPath();
    x = e.pageX;
    y = e.pageY-44;
    ctx.moveTo(x,y);
  };
  var move = function(e) {
    e.preventDefault();
        e = e.originalEvent;
    x = e.pageX;
    y = e.pageY-44;
    ctx.lineTo(x,y);
    ctx.stroke();
    };
  $(this).on("MSPointerDown", start);
  $(this).on("MSPointerMove", move);
};
