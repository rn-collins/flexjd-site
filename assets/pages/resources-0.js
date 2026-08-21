
(function(){
  var input=document.getElementById('resSearchInput');
  var clearBtn=document.getElementById('resSearchClear');
  var status=document.getElementById('resSearchStatus');
  if(!input) return;
  var faqs=[].slice.call(document.querySelectorAll('details.faq'));
  var rows=[].slice.call(document.querySelectorAll('table.data tbody tr'));
  var frames=[].slice.call(document.querySelectorAll('.frame'));
  var sections=[].slice.call(document.querySelectorAll('main > .csec[id^="r"]'));
  var totalItems=faqs.length+rows.length+frames.length;

  function itemMatches(el,terms){
    var text=el.textContent.toLowerCase();
    return terms.every(function(t){return text.indexOf(t)!==-1;});
  }

  function runFilter(){
    var q=input.value.trim().toLowerCase();
    clearBtn.hidden=!q;
    if(!q){
      faqs.forEach(function(el){el.classList.remove('res-hidden');el.open=false;});
      rows.forEach(function(el){el.classList.remove('res-hidden');});
      frames.forEach(function(el){el.classList.remove('res-hidden');});
      sections.forEach(function(s){s.classList.remove('res-empty');});
      status.textContent='';
      return;
    }
    var terms=q.split(/\s+/).filter(Boolean);
    var visibleCount=0;
    faqs.forEach(function(el){
      var match=itemMatches(el,terms);
      el.classList.toggle('res-hidden',!match);
      if(match){visibleCount++;el.open=true;}
    });
    rows.forEach(function(el){
      var match=itemMatches(el,terms);
      el.classList.toggle('res-hidden',!match);
      if(match)visibleCount++;
    });
    frames.forEach(function(el){
      var match=itemMatches(el,terms);
      el.classList.toggle('res-hidden',!match);
      if(match)visibleCount++;
    });
    sections.forEach(function(s){
      var anyVisible=s.querySelector('details.faq:not(.res-hidden), tbody tr:not(.res-hidden), .frame:not(.res-hidden)');
      var hasSearchables=s.querySelector('details.faq, tbody tr, .frame');
      s.classList.toggle('res-empty', !!hasSearchables && !anyVisible);
    });
    status.innerHTML='<strong>'+visibleCount+'</strong> matching items for "'+input.value.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'"';
  }
  input.addEventListener('input',runFilter);
  clearBtn.addEventListener('click',function(){input.value='';runFilter();input.focus();});
  document.addEventListener('keydown',function(e){
    if(e.key==='/' && document.activeElement!==input && !/input|textarea/i.test(document.activeElement.tagName)){
      e.preventDefault();input.focus();
    }
  });
})();
