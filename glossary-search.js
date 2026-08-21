(function () {
  var input = document.getElementById('glSearchInput');
  var clearBtn = document.getElementById('glSearchClear');
  var status = document.getElementById('glSearchStatus');
  if (!input) return;
  var termsAll = [].slice.call(document.querySelectorAll('details.faq'));
  var sections = [].slice.call(document.querySelectorAll('main > .csec[id^="g"]'));
  function runFilter() {
    var query = input.value.trim().toLowerCase();
    clearBtn.hidden = !query;
    if (!query) {
      termsAll.forEach(function (el) { el.classList.remove('gl-hidden'); el.open = false; });
      sections.forEach(function (el) { el.classList.remove('gl-empty'); });
      status.textContent = '';
      return;
    }
    var queryTerms = query.split(/\s+/).filter(Boolean);
    var count = 0;
    termsAll.forEach(function (el) {
      var value = el.textContent.toLowerCase();
      var match = queryTerms.every(function (term) { return value.indexOf(term) !== -1; });
      el.classList.toggle('gl-hidden', !match);
      if (match) { count++; el.open = true; }
    });
    sections.forEach(function (section) { section.classList.toggle('gl-empty', !section.querySelector('details.faq:not(.gl-hidden)')); });
    status.textContent = count + ' of ' + termsAll.length + ' terms match “' + input.value + '”';
  }
  input.addEventListener('input', runFilter);
  clearBtn.addEventListener('click', function () { input.value = ''; runFilter(); input.focus(); });
  document.addEventListener('keydown', function (event) {
    var active = document.activeElement;
    if (event.key === '/' && !event.defaultPrevented && !event.ctrlKey && !event.metaKey && !event.altKey && active !== input && !/input|textarea|select/i.test(active.tagName) && !active.isContentEditable) {
      event.preventDefault(); input.focus();
    }
  });
})();
