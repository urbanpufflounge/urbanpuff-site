/* Urban Puff — form delivery endpoint.
   A FormSubmit hashed endpoint. The inbox address does not appear
   anywhere in this site.
   The endpoint is never written into the HTML or into the DOM: it is held in a
   closure here and handed to the submit handler only at the moment of sending,
   so nothing a crawler renders or a scraper parses contains the address.
   Set SITE["form_token"] in tools/build.py; this file is generated. */
(function () {
  'use strict';
  var T = '107255ed9e810f4577564bb36d288488';
  var HASHED = true;
  var to = HASHED ? T : (window.atob ? window.atob(T) : '');
  window.UP_FORM_TARGET = function (ajax) {
    if (!to) return '';
    return 'https://formsubmit.co/' + (ajax ? 'ajax/' : '') + to;
  };
})();
