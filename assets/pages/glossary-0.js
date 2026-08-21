
(function(){

  var input=document.getElementById('glSearchInput');
  var clearBtn=document.getElementById('glSearchClear');
  var status=document.getElementById('glSearchStatus');
  if(input){
    var terms_all=[].slice.call(document.querySelectorAll('details.faq'));
    var sections=[].slice.call(document.querySelectorAll('main > .csec[id^="g"]'));
    var total=terms_all.length;
    function runFilter(){
      var q=input.value.trim().toLowerCase();
      clearBtn.hidden=!q;
      if(!q){
        terms_all.forEach(function(el){el.classList.remove('gl-hidden');el.open=false;});
        sections.forEach(function(s){s.classList.remove('gl-empty');});
        status.textContent='';
        return;
      }
      var qterms=q.split(/\s+/).filter(Boolean);
      var count=0;
      terms_all.forEach(function(el){
        var text=el.textContent.toLowerCase();
        var match=qterms.every(function(t){return text.indexOf(t)!==-1;});
        el.classList.toggle('gl-hidden',!match);
        if(match){count++;el.open=true;}
      });
      sections.forEach(function(s){
        var any=s.querySelector('details.faq:not(.gl-hidden)');
        s.classList.toggle('gl-empty', !any);
      });
      status.innerHTML='<strong>'+count+'</strong> of '+total+' terms match "'+input.value.replace(/</g,'&lt;')+'"';
    }
    input.addEventListener('input',runFilter);
    clearBtn.addEventListener('click',function(){input.value='';runFilter();input.focus();});
    document.addEventListener('keydown',function(e){
      if(e.key==='/' && document.activeElement!==input && !/input|textarea/i.test(document.activeElement.tagName)){
        e.preventDefault();input.focus();
      }
    });
  }
})();
