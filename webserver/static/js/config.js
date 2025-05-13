document.addEventListener('DOMContentLoaded', function() {
  // Handle back/forward navigation
  /*window.addEventListener('popstate', function(event) {
    if(event.state && event.state.htmx) {
          htmx.ajax('GET', window.location.pathname, {
              target: '#main-content',
              swap: 'innerHTML'
          });
    }
  });*/
  
  // loading indicator before each request
  document.body.addEventListener('htmx:beforeRequest', function(event) {
    // CSS on static/css
    document.getElementById('main-content').innerHTML = `
      <div class="loading">
        <div class="spinner"></div>
        <div class="loading-text">Loading...</div>
      </div>
    `;
  });

  htmx.defineExtension('debug', {
    onEvent: function (name, evt) {
      if (console.debug) console.debug(name, evt);
      else if (console) console.log("DEBUG:", name, evt);
      else throw "NO CONSOLE SUPPORTED";
    }
  });
});

