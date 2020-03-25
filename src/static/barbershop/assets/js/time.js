var auto_refresh = setInterval(
    function ()
    {
    $(' .time').load(' .time');
    }, 10000); 
var auto_time_refresh = setInterval(
    function ()
    {
    $(' .timename').load(' .timename');
    }, 10000); 

var auto_weather_refresh = setInterval(
    function ()
    {
    $(' .weather-link').load(' .weather-link');
    }, 10000); 

var services_refresh = setInterval(
    function ()
    {
    $(' .services').load(' .services');
    }, 10000); 