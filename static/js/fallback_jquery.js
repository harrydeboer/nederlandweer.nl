if (!window.jQuery) {
    let myScript = document.createElement('script');

    myScript.setAttribute('src','/dist/jquery.min.js');

    document.head.append(myScript);

    function defer() {
        if (!window.jQuery) {
            setTimeout(function() { defer(); }, 50);
        }
    }
    defer();
}
