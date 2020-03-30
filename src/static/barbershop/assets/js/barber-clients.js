var auto_refresh = setInterval(
    function ()
    {
    $(' .barber-clients').load(' .barber-clients');
    }, 3000);