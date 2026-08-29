document.addEventListener('DOMContentLoaded',function(){
  var input=document.getElementById('oppSearchInput');
  var clear=document.getElementById('oppSearchClear');
  var message=document.getElementById('oppSearchStatus');
  var rows=[].slice.call(document.querySelectorAll('tr[data-listing="true"]'));
  var sections=[].slice.call(document.querySelectorAll('main section.csec[id^="o"]'));
  var category='all', status='all';
  var labels={historical:'Historical record',upcoming:'Future date in record · unverified',rolling:'Rolling language · unverified','needs-review':'Needs primary-source review'};
  var verificationLabels={'source-checked':'Official destination checked','primary-current':'Current terms source-checked','primary-historical':'Historical terms source-checked','primary-closed':'Closed cycle source-checked'};
  // A "terms" check confirmed the claims recorded here against the sponsor's own page.
  // 'source-checked' confirmed only that the link still reaches the official destination.
  var termsChecked={'primary-current':1,'primary-historical':1,'primary-closed':1};

  rows.forEach(function(row){
    var cell=row.querySelector('td'), value=row.getAttribute('data-status');
    if(!cell || !labels[value]) return;
    var badge=document.createElement('span');
    badge.className='record-status record-status--'+value;
    badge.textContent=labels[value];
    badge.title=row.getAttribute('data-status-reason')||'';
    cell.prepend(badge);
    var verification=row.getAttribute('data-verification');
    if(verificationLabels[verification]){
      var verifiedBadge=document.createElement('span');
      verifiedBadge.className='record-status record-status--source-checked';
      verifiedBadge.textContent=verificationLabels[verification];
      cell.prepend(verifiedBadge);
    }
    row.querySelectorAll('a.apply-link').forEach(function(link){
      var sourceChecked=Boolean(verificationLabels[verification]);
      var isHistorical=value==='historical';
      link.textContent=sourceChecked?(isHistorical?'Open checked historical source →':'Open checked primary source →'):(isHistorical?'Official archive/source →':'Check official source →');
      link.setAttribute('aria-label',((sourceChecked?(isHistorical?'Open checked historical source for ':'Open checked primary source for '):(isHistorical?'Open official archive or source for ':'Check current status with official source for '))+(cell.textContent||'this record').replace(labels[value],'').replace(verificationLabels[verification]||'','').trim()));
    });
  });

  // Derive the header summary from the records themselves so it can never drift
  // from the live counter below or from the data.
  var summary=document.getElementById('oppVerificationSummary');
  if(summary){
    var counts={};
    rows.forEach(function(row){var v=row.getAttribute('data-verification')||'none';counts[v]=(counts[v]||0)+1;});
    var nCurrent=counts['primary-current']||0,nHistorical=counts['primary-historical']||0,nClosed=counts['primary-closed']||0;
    var nDestination=counts['source-checked']||0;
    var nTerms=nCurrent+nHistorical+nClosed;
    var nNone=rows.length-nTerms-nDestination;
    var text='Of '+rows.length+' records, '+nTerms+' have had their recorded terms checked against the sponsor’s own page ('+nCurrent+' current-cycle, '+nHistorical+' historical, '+nClosed+' closed cycle) and '+nDestination+' have had only the official destination confirmed';
    summary.textContent=text+(nNone?('; '+nNone+' carry no source check.'):'.');
  }

  function setChips(selector,attribute,value){
    document.querySelectorAll(selector).forEach(function(chip){
      var on=chip.getAttribute(attribute)===value;
      chip.classList.toggle('is-active',on); chip.setAttribute('aria-pressed',String(on));
    });
  }
  function applyFilters(){
    var query=input ? input.value.trim().toLowerCase() : '';
    var terms=query.split(/\s+/).filter(Boolean), visible=0;
    rows.forEach(function(row){
      var section=row.closest('section.csec');
      var matchCategory=category==='all'||(section&&section.id===category);
      var matchStatus=status==='all'||row.getAttribute('data-status')===status;
      var text=(row.textContent||'').toLowerCase();
      var matchText=terms.every(function(term){return text.indexOf(term)!==-1;});
      var show=matchCategory&&matchStatus&&matchText;
      row.classList.toggle('opp-hidden',!show); if(show) visible++;
    });
    sections.forEach(function(section){
      section.querySelectorAll('tr[data-listing="false"]').forEach(function(group){
        var next=group.nextElementSibling, show=false;
        while(next && next.getAttribute('data-listing')==='true'){
          if(!next.classList.contains('opp-hidden')){show=true;break;}
          next=next.nextElementSibling;
        }
        group.classList.toggle('opp-hidden',!show);
      });
      section.classList.toggle('opp-empty-cat',!section.querySelector('tr[data-listing="true"]:not(.opp-hidden)'));
    });
    if(clear) clear.hidden=!query;
    if(message){
      var shown=rows.filter(function(row){return !row.classList.contains('opp-hidden');});
      var shownTerms=shown.filter(function(row){return termsChecked[row.getAttribute('data-verification')];}).length;
      var shownDestination=shown.filter(function(row){return row.getAttribute('data-verification')==='source-checked';}).length;
      message.textContent=visible+' of '+rows.length+' records shown; '+shownTerms+' with their recorded terms checked against the sponsor’s own page, '+shownDestination+' with the official destination confirmed only. Status badges and source-check badges describe different things.';
    }
  }
  document.querySelectorAll('[data-cat]').forEach(function(chip){chip.addEventListener('click',function(){category=chip.getAttribute('data-cat');setChips('[data-cat]','data-cat',category);applyFilters();});});
  document.querySelectorAll('[data-opp-status]').forEach(function(chip){chip.addEventListener('click',function(){status=chip.getAttribute('data-opp-status');setChips('[data-opp-status]','data-opp-status',status);applyFilters();});});
  if(input) input.addEventListener('input',applyFilters);
  if(clear) clear.addEventListener('click',function(){input.value='';applyFilters();input.focus();});
  document.addEventListener('keydown',function(event){
    if(event.key==='/'&&!event.ctrlKey&&!event.metaKey&&!event.altKey&&input&&!/input|textarea|select/i.test(document.activeElement.tagName)){event.preventDefault();input.focus();}
    if(event.key==='Escape'&&input&&document.activeElement===input&&input.value){input.value='';applyFilters();}
  });
  applyFilters();
});
