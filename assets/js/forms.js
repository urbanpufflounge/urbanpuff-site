/* Urban Puff — form delivery endpoint.
   The address, base64-encoded. This keeps it out of the page source
   and away from mail harvesters and crawlers, but anyone who reads
   this file can decode it. To remove it properly, set
   SITE["form_token"] = "hash:<your FormSubmit string>" and rebuild.
   The endpoint is never written into the HTML or into the DOM: it is held in a
   closure here and handed to the submit handler only at the moment of sending,
   so nothing a crawler renders or a scraper parses contains the address.
   Set SITE["form_token"] in tools/build.py; this file is generated. */
(function () {
  'use strict';
  var T = 'dXJiYW5wdWZmMUBnbWFpbC5jb20=';
  var HASHED = false;
  var to = HASHED ? T : (window.atob ? window.atob(T) : '');
  window.UP_FORM_TARGET = function (ajax) {
    if (!to) return '';
    return 'https://formsubmit.co/' + (ajax ? 'ajax/' : '') + to;
  };
})();
