window.onload = function(){
  drawSetup($('canvas'),$('canvas2'));
}
var model;
function onFileSelect(e) { var f = e.target.files;
  var reader = new FileReader();
  reader.onload = function(filename){
    var fs = new Float32Stream(reader.result);
    model = new Model(fs);
    $('checkButton').disabled = "";
  }
  reader.readAsArrayBuffer(f[0]);
}
function check(){
  var Data = getX($('canvas'));
  var xData = JSON.stringify({"x":Data});
  jQuery.ajax({
    type:'POST',
    url:'/postText',
    data:xData,
    contentType:'application/json; charset=utf-8',
    success:function(data) {
      var result = JSON.parse(data.ResultSet).result;
      document.getElementById("hello").innerText = "値は" + result + "です";
    }
  });
}

function allClear(){
  canvasClear($('canvas'));
  canvasClear($('canvas2'));
}

function $(id){
  return document.getElementById(id);
}
