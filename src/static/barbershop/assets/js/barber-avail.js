var auto_refresh = setInterval(
    function ()
    {
    $(' #barber-avail').load(' #barber-avail');
    }, 3000);