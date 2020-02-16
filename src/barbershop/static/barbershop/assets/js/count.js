var auto_refresh = setInterval(
    function ()
    {
    $(' .count').load(' .count');
    }, 10000); 