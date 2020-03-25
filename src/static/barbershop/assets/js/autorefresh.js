var auto_refresh = setInterval(
    function ()
    {
    $(' .client').load(' .client');
    }, 3000);
    