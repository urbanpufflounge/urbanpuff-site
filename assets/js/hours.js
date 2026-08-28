/* ==========================================================================
   Urban Puff — opening hours
   --------------------------------------------------------------------------
   Two layers:

   1. ALWAYS: the hours written into the HTML render immediately, and an
      "Open now / Closed" badge is computed from them in the venue's own
      timezone. Works with no network, no key, no cost.

   2. OPTIONAL: if you fill in CONFIG below, the page also asks the Google
      Places API for the live hours on that listing and replaces what's on
      screen. If the call fails for any reason, layer 1 stays put — the page
      never ends up blank or wrong.

   To switch layer 2 on:
     a. Find your Place ID:  https://developers.google.com/maps/documentation/places/web-service/place-id
     b. Google Cloud Console -> enable "Places API (New)" -> create an API key
     c. RESTRICT THE KEY. Application restriction: "Websites", allow
        https://urbanpufflounge.com/*  and  https://www.urbanpufflounge.com/*
        API restriction: Places API (New) only.
        The key is visible in this file — restriction is what keeps it safe.
     d. Paste both values below and push.
   ========================================================================== */

(function () {
  'use strict';

  var CONFIG = {
    placeId: '',   // e.g. 'ChIJ....'
    apiKey: ''     // e.g. 'AIza....'  — must be referrer-restricted
  };

  var TZ = 'America/New_York';

  var panel = document.querySelector('[data-hours]');
  if (!panel) return;

  var badge = panel.querySelector('[data-hours-status]');
  var list = panel.querySelector('[data-hours-list]');
  var note = panel.querySelector('[data-hours-note]');

  /* ---------- local time in the venue's timezone ---------- */
  function venueNow() {
    try {
      var parts = new Intl.DateTimeFormat('en-US', {
        timeZone: TZ, weekday: 'short', hour: '2-digit',
        minute: '2-digit', hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      return {
        day: days[map.weekday],
        minutes: parseInt(map.hour, 10) * 60 + parseInt(map.minute, 10)
      };
    } catch (e) {
      var d = new Date();
      return { day: d.getDay(), minutes: d.getHours() * 60 + d.getMinutes() };
    }
  }

  function toMinutes(hhmm) {
    var bits = String(hhmm).split(':');
    return parseInt(bits[0], 10) * 60 + parseInt(bits[1] || '0', 10);
  }

  /* ---------- layer 1: compute open/closed from the baked-in hours ---------- */
  function readBakedHours() {
    var el = panel.querySelector('[data-hours-data]');
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  function isOpen(blocks, now) {
    for (var i = 0; i < blocks.length; i++) {
      var b = blocks[i];
      var open = toMinutes(b.open);
      var close = toMinutes(b.close);   // may exceed 1440 = closes after midnight
      for (var j = 0; j < b.days.length; j++) {
        var d = b.days[j];
        // same-day window
        if (d === now.day && now.minutes >= open && now.minutes < close) return true;
        // window that started yesterday and runs past midnight
        if (close > 1440) {
          var prev = (d + 1) % 7;
          if (prev === now.day && now.minutes < close - 1440) return true;
        }
      }
    }
    return false;
  }

  function setBadge(open, label) {
    if (!badge) return;
    badge.setAttribute('data-state', open ? 'open' : 'closed');
    badge.textContent = label || (open ? 'Open now' : 'Closed right now');
  }

  function markToday(now) {
    var rows = panel.querySelectorAll('.hours-row[data-days]');
    Array.prototype.forEach.call(rows, function (row) {
      var days = row.getAttribute('data-days').split(',').map(Number);
      row.setAttribute('data-today', days.indexOf(now.day) !== -1 ? 'true' : 'false');
    });
  }

  var blocks = readBakedHours();
  var now = venueNow();
  if (blocks) {
    setBadge(isOpen(blocks, now));
    markToday(now);
  } else if (badge) {
    badge.remove();
  }

  /* ---------- layer 2: live hours from Google ---------- */
  if (!CONFIG.placeId || !CONFIG.apiKey) return;

  var url = 'https://places.googleapis.com/v1/places/' +
    encodeURIComponent(CONFIG.placeId) +
    '?fields=regularOpeningHours.weekdayDescriptions,currentOpeningHours.openNow' +
    '&key=' + encodeURIComponent(CONFIG.apiKey);

  fetch(url, { headers: { 'Accept': 'application/json' } })
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (data) {
      var desc = data &&
        data.regularOpeningHours &&
        data.regularOpeningHours.weekdayDescriptions;
      if (!desc || !desc.length || !list) return;

      // Google returns Monday-first: "Monday: 4:00 PM – 12:00 AM"
      var order = [1, 2, 3, 4, 5, 6, 0];
      var html = desc.map(function (line, i) {
        var split = line.indexOf(':');
        var day = split === -1 ? line : line.slice(0, split);
        var time = split === -1 ? '' : line.slice(split + 1).trim();
        return '<div class="hours-row" data-days="' + order[i] + '">' +
          '<span>' + day + '</span><span>' + (time || 'Closed') + '</span></div>';
      }).join('');

      list.innerHTML = html;
      markToday(venueNow());

      var live = data.currentOpeningHours && data.currentOpeningHours.openNow;
      if (typeof live === 'boolean') setBadge(live);

      if (note) note.textContent = 'Live from our Google listing.';
      panel.setAttribute('data-source', 'google');
    })
    .catch(function () {
      /* keep the baked-in hours — nothing to do */
    });
})();
