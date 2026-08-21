(function () {
  var input = document.getElementById('resSearchInput');
  var clearBtn = document.getElementById('resSearchClear');
  var status = document.getElementById('resSearchStatus');
  if (!input) return;
  var faqs = [].slice.call(document.querySelectorAll('details.faq'));
  var rows = [].slice.call(document.querySelectorAll('table.data tbody tr'));
  var frames = [].slice.call(document.querySelectorAll('.frame'));
  var sections = [].slice.call(document.querySelectorAll('main > .csec[id^="r"]'));
  var priorFaqState = null;
  function itemMatches(el, terms) {
    var value = el.textContent.toLowerCase();
    return terms.every(function (term) { return value.indexOf(term) !== -1; });
  }
  function runFilter() {
    var query = input.value.trim().toLowerCase();
    clearBtn.hidden = !query;
    if (!query) {
      faqs.forEach(function (el, index) { el.classList.remove('res-hidden'); if (priorFaqState) el.open = priorFaqState[index]; });
      rows.forEach(function (el) { el.classList.remove('res-hidden'); });
      frames.forEach(function (el) { el.classList.remove('res-hidden'); });
      sections.forEach(function (el) { el.classList.remove('res-empty'); });
      status.textContent = '';
      priorFaqState = null;
      return;
    }
    if (!priorFaqState) priorFaqState = faqs.map(function (el) { return el.open; });
    var terms = query.split(/\s+/).filter(Boolean);
    var visibleCount = 0;
    [faqs, rows, frames].forEach(function (collection) {
      collection.forEach(function (el) {
        var match = itemMatches(el, terms);
        el.classList.toggle('res-hidden', !match);
        if (match) { visibleCount++; if (el.tagName === 'DETAILS') el.open = true; }
      });
    });
    sections.forEach(function (section) {
      var anyVisible = section.querySelector('details.faq:not(.res-hidden), tbody tr:not(.res-hidden), .frame:not(.res-hidden)');
      var hasSearchables = section.querySelector('details.faq, tbody tr, .frame');
      section.classList.toggle('res-empty', !!hasSearchables && !anyVisible);
    });
    status.textContent = visibleCount + ' matching items for “' + input.value + '”';
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
