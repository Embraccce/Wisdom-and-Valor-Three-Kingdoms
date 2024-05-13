(function () {
  var accountId;
  var visitorIdKey = "Metadata_visitor_id";
  var sessionIdKey = "Metadata_session_id";
  var baseUrl = "https://api-gw.metadata.io";
  var blacklistIds = [1721];

  function getCookieValue(key) {
    var cookie = document.cookie.split("; ").find(function (cookie) {
      return cookie.indexOf(key) === 0;
    });

    if (cookie) {
      return cookie.split("=")[1];
    }

    return null;
  }

  function setCookieValue(key, value, expires) {
    document.cookie = key + "=" + value + "; expires=" + expires + "; path=/";
  }

  function createId() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
  }

  function createCookieExpiration(minutes) {
    return new Date(new Date().getTime() + 1000 * 60 * minutes).toGMTString();
  }

  var visitorId = (function () {
    var storedVisitorId = getCookieValue(visitorIdKey);

    if (storedVisitorId) {
      return storedVisitorId;
    }

    var visitorId = createId();
    var expires = createCookieExpiration(525600); // 1 year from now

    setCookieValue(visitorIdKey, visitorId, expires);
    return visitorId;
  })();

  var sessionId = (function () {
    var storedSessionId = getCookieValue(sessionIdKey);

    if (storedSessionId) {
      return storedSessionId;
    }

    var sessionId = createId();
    var expires = createCookieExpiration(30);

    setCookieValue(sessionIdKey, sessionId, expires);
    return sessionId;
  })();

  function recordTraffic() {
    fetch(baseUrl + "/traffic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: window.location.href,
        url_referrer: window.document.referrer,
        account_id: accountId,
        session_id: sessionId,
        visitor_id: visitorId
      })
    });
  }

  function prolongSession() {
    var storedSessionId = getCookieValue(sessionIdKey);

    if (storedSessionId) {
      var expires = createCookieExpiration(30);
      setCookieValue(sessionIdKey, storedSessionId, expires);
    }
  }

  function throttle(func, timeFrame) {
    var lastTime = 0;

    return function (...args) {
      var now = new Date();

      if (now - lastTime >= timeFrame) {
        func(...args);
        lastTime = now;
      }
    };
  }

  function init(options) {
    if (options.baseUrl) {
      baseUrl = options.baseUrl;
    }

    if (options.accountId) {
      accountId = options.accountId;
    }

    window.addEventListener("scroll", throttle(prolongSession, 1000));
    window.addEventListener("click", throttle(prolongSession, 1000));

    if (!blacklistIds.includes(accountId)) {
      recordTraffic();
    }
  }

  window.Metadata = window.Metadata || {};
  window.Metadata.siteInsights = { init };
})();
