function getAjax(url, success) {
    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        xhr.open('GET', url);
        xhr.onreadystatechange = function() {
                    if (xhr.readyState>3 && xhr.status==200) success(xhr.responseText);
                };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send();
        return xhr;
}

// example request
getAjax('http://singlepoint.space:5000/api', function(data){ console.log(data); temp='test' });

var d3script = document.createElement('script');  
d3script.setAttribute('src','https://cdn.plot.ly/plotly-latest.min.js');
document.head.appendChild(d3script);

var b = document.getElementsByTagName('body')[0]
var d = document.createElement("div")
d.id = "graphdiv2"
b.append(d)

var trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  mode: 'markers',
  type: 'scatter'
};

var trace2 = {
  x: [2, 3, 4, 5],
  y: [16, 5, 11, 9],
  mode: 'lines',
  type: 'scatter'
};

var trace3 = {
  x: [1, 2, 3, 4],
  y: [12, 9, 15, 12],
  mode: 'lines+markers',
  type: 'scatter'
};

var data = [trace1, trace2, trace3];

setTimeout(function(){ Plotly.newPlot('graphdiv2', data)}, 500);