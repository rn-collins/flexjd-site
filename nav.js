(function(){
  var nav=document.querySelector('.nav');
  var onscroll=function(){if(nav)nav.classList.toggle('scrolled',window.scrollY>12);};
  window.addEventListener('scroll',onscroll,{passive:true});onscroll();
  var tg=document.querySelector('.nav__toggle'),lk=document.querySelector('.nav__links'),priorFocus=null;
  function mobileOpen(){return !!(tg&&lk&&lk.classList.contains('open'));}
  function closeMobile(restore){if(!tg||!lk)return;lk.classList.remove('open');tg.setAttribute('aria-expanded','false');tg.setAttribute('aria-label','Open navigation menu');if(restore&&priorFocus)priorFocus.focus();priorFocus=null;}
  function openMobile(){if(!tg||!lk)return;priorFocus=document.activeElement;lk.classList.add('open');tg.setAttribute('aria-expanded','true');tg.setAttribute('aria-label','Close navigation menu');var first=lk.querySelector('a,button,[tabindex]:not([tabindex="-1"])');if(first)first.focus();}
  if(tg&&lk){
    tg.addEventListener('click',function(){mobileOpen()?closeMobile(false):openMobile();});
    lk.addEventListener('click',function(e){if(e.target.closest('a')&&mobileOpen())closeMobile(false);});
    window.addEventListener('resize',function(){if(window.innerWidth>880&&mobileOpen())closeMobile(false);});
  }
  document.querySelectorAll('.nav__dd').forEach(function(dd){
    var db=dd.querySelector('.nav__ddbtn');
    if(!dd||!db)return;
    var menu=dd.querySelector('.nav__mega');
    if(menu&&!menu.id)menu.id='nav-menu-'+Math.random().toString(36).slice(2,9);
    if(menu)db.setAttribute('aria-controls',menu.id);
    db.addEventListener('click',function(e){e.stopPropagation();document.querySelectorAll('.nav__dd.open').forEach(function(other){if(other!==dd){other.classList.remove('open');var ob=other.querySelector('.nav__ddbtn');if(ob)ob.setAttribute('aria-expanded','false');}});var o=dd.classList.toggle('open');db.setAttribute('aria-expanded',o);});
    document.addEventListener('click',function(e){if(!dd.contains(e.target)){dd.classList.remove('open');db.setAttribute('aria-expanded','false');}});
    dd.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();dd.classList.remove('open');db.setAttribute('aria-expanded','false');db.focus();}});
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&mobileOpen()){e.preventDefault();closeMobile(true);return;}
    if(e.key==='Tab'&&mobileOpen()){
      var focusable=[].slice.call(lk.querySelectorAll('a,button,[tabindex]:not([tabindex="-1"])')).filter(function(el){return !el.disabled&&el.offsetParent!==null;});
      if(!focusable.length)return;var first=focusable[0],last=focusable[focusable.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  var tt=document.querySelector('.totop');
  if(tt){window.addEventListener('scroll',function(){tt.classList.toggle('show',window.scrollY>700);},{passive:true});tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});}
  var sn=document.querySelector('.secnav');
  if(sn){var links=[].slice.call(sn.querySelectorAll('a'));var secs=links.map(function(l){return document.querySelector(l.getAttribute('href'));}).filter(Boolean);
    links.forEach(function(l){l.addEventListener('click',function(){var target=document.querySelector(l.getAttribute('href'));if(target){target.setAttribute('tabindex','-1');setTimeout(function(){target.focus({preventScroll:true});},0);}});});
    var spy=function(){var y=window.scrollY+120;var cur=secs[0];secs.forEach(function(s){if(s&&s.offsetTop<=y)cur=s;});links.forEach(function(l){var active=cur&&l.getAttribute('href')==='#'+cur.id;l.classList.toggle('active',active);if(active)l.setAttribute('aria-current','location');else l.removeAttribute('aria-current');});};
    window.addEventListener('scroll',spy,{passive:true});spy();}
  document.querySelectorAll('.tbl').forEach(function(wrapper,i){
    var section=wrapper.closest('section'),heading=section&&section.querySelector('h2,h3'),table=wrapper.querySelector('table');
    if(heading&&!heading.id)heading.id='table-section-'+(i+1);
    wrapper.setAttribute('tabindex','0');wrapper.setAttribute('role','region');
    if(heading)wrapper.setAttribute('aria-labelledby',heading.id);else wrapper.setAttribute('aria-label','Scrollable data table');
    var hint=document.createElement('span');hint.className='table-scroll-hint';hint.id='table-scroll-hint-'+(i+1);hint.textContent='Scroll horizontally to view all columns.';wrapper.insertAdjacentElement('beforebegin',hint);wrapper.setAttribute('aria-describedby',hint.id);
    if(table&&!table.querySelector('caption')&&heading){var caption=document.createElement('caption');caption.className='sr-only';caption.textContent=heading.textContent.trim();table.prepend(caption);}
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  }else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});}
})();
