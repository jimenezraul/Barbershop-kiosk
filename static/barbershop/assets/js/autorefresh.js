var auto_refresh = setInterval(
    function ()
    {
    $(' .clients').load(' .clients');
    }, 3000);
    