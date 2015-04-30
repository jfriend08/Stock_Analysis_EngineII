# Front-end frameworks

* Boostrap
http://getbootstrap.com
* JQuery
* Highcharts 
http://www.highcharts.com/demo

###Techniques:
HTML as the base, and add the Boostrap framework which help improve the css style and some basic JavaScript animation effects. Using JQuery because the framework Highchars is based on JQuery. 

When you want to add a new animated diagram into the website, just add a empty div tag

```
<div id="container" style="width:70%; height:300px;"></div>
```

and create a new JavaScript file, maybe name it "tmp.js".
add the js code from Highcharts's official website's demo, for example, like 

attention that the ``` '#container' ``` should has the same id name (```div id="container"```) as the html tag above.

```
$(function () {
    $('#container').highcharts({
        chart: {
            type: 'spline',
            inverted: true
        },
        title: {
            text: 'Atmosphere Temperature by Altitude'
        },
        subtitle: {
            text: 'According to the Standard Atmosphere Model'
        },
        xAxis: {
            reversed: false,
            title: {
                enabled: true,
                text: 'Altitude'
            },
            labels: {
                formatter: function () {
                    return this.value + 'km';
                }
            },
            maxPadding: 0.05,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Temperature'
            },
            labels: {
                formatter: function () {
                    return this.value + '°';
                }
            },
            lineWidth: 2
        },
        legend: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br/>',
            pointFormat: '{point.x} km: {point.y}°C'
        },
        plotOptions: {
            spline: {
                marker: {
                    enable: false
                }
            }
        },
        series: [{
            name: 'Temperature',
            data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
                [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
        }]
    });
});

```

after that, add that js file's reference into the bottom of the html file, like
``` <script src="js/tmp.js"></script> ``` . Pay attention that it must after the reference of boostrap and jQuery, or else it won't work.



