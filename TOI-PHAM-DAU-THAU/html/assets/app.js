(function () {
  var KEY = 'stdtv-theme';
  var btn = document.getElementById('themeBtn');
  try {
    var saved = localStorage.getItem(KEY);
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch (e) {}
  if (btn) {
    btn.addEventListener('click', function () {
      var now = document.documentElement.getAttribute('data-theme');
      var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      var next = now ? (now === 'dark' ? 'light' : 'dark') : (prefersDark ? 'light' : 'dark');
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
  }
  var tables = document.querySelectorAll('main table');
  for (var i = 0; i < tables.length; i++) {
    var tb = tables[i];
    if (tb.parentElement && tb.parentElement.className === 'tablewrap') continue;
    var d = document.createElement('div');
    d.className = 'tablewrap';
    tb.parentNode.insertBefore(d, tb);
    d.appendChild(tb);
  }
})();
