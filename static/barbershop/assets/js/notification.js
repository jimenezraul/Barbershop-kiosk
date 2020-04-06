var auto_refresh = setInterval(
    function ()
    {
    $(' #notification').load(' #notification');
    }, 3000); 