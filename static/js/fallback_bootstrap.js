if($('body').css('color') !== 'rgb(33, 37, 41)') {
    $("head").prepend('<link rel="stylesheet" href="/static/css/bootstrap.min.css">');
}

window.bootstrap || document.write('<script type="text/javascript" ' +
    'src="/static/dist/bootstrap.bundle.min.js"><\/script>');
