function loadPage(iframe) {
    if (!loaded) {
        let urlParams = new URLSearchParams(window.location.search);
        let sub = urlParams.get('sub');

        if (sub) {
            let basePath = window.location.pathname.replace(/\/support\/?$/, '');
            let newUrl = basePath + '/' + sub;
            window.location.replace(newUrl);
            }

        loaded = true;
        }
    }
