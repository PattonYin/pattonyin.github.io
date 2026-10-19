// Paste the public token from Cloudflare Web Analytics > Manage site here.
// Leave empty to disable analytics. This is not a Cloudflare API key.
(() => {
    const token = '20bf553324ac4c54b2aa6b351e9f43da';
    const { hostname, pathname, search, protocol } = window.location;
    if (!token || !/^https?:$/.test(protocol)
        || ['localhost', '127.0.0.1', '[::1]'].includes(hostname)) return;

    // The destination page records the view after a legacy-link redirect.
    const parameters = new URLSearchParams(search);
    if ((pathname.endsWith('/portfolio.html') && parameters.has('project'))
        || (pathname.endsWith('/rollouts.html') && parameters.has('robot'))) return;

    if (document.querySelector('script[data-cf-beacon]')) return;
    const beacon = document.createElement('script');
    beacon.type = 'module';
    beacon.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    // Full page loads have distinct paths; section anchors are not separate page views.
    beacon.dataset.cfBeacon = JSON.stringify({ token, spa: false });
    document.head.append(beacon);
})();
