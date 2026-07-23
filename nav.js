(function(){
  var nav=document.querySelector('.nav');
  var onscroll=function(){if(nav)nav.classList.toggle('scrolled',window.scrollY>12);};
  window.addEventListener('scroll',onscroll,{passive:true});onscroll();
  var tg=document.querySelector('.nav__toggle'),lk=document.querySelector('.nav__links');
  if(tg&&lk)tg.addEventListener('click',function(){var o=lk.classList.toggle('open');tg.setAttribute('aria-expanded',o);});
  document.querySelectorAll('.nav__dd').forEach(function(dd){
    var db=dd.querySelector('.nav__ddbtn');
    if(!dd||!db)return;
    db.addEventListener('click',function(e){e.stopPropagation();var o=dd.classList.toggle('open');db.setAttribute('aria-expanded',o);});
    document.addEventListener('click',function(e){if(!dd.contains(e.target)){dd.classList.remove('open');db.setAttribute('aria-expanded','false');}});
    db.addEventListener('keydown',function(e){if(e.key==='Escape'){dd.classList.remove('open');db.setAttribute('aria-expanded','false');db.focus();}});
  });
  var tt=document.querySelector('.totop');
  if(tt){window.addEventListener('scroll',function(){tt.classList.toggle('show',window.scrollY>700);},{passive:true});tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});}
  var sn=document.querySelector('.secnav');
  if(sn){var links=[].slice.call(sn.querySelectorAll('a'));var secs=links.map(function(l){return document.querySelector(l.getAttribute('href'));}).filter(Boolean);
    var spy=function(){var y=window.scrollY+120;var cur=secs[0];secs.forEach(function(s){if(s&&s.offsetTop<=y)cur=s;});links.forEach(function(l){l.classList.toggle('active',cur&&l.getAttribute('href')==='#'+cur.id);});};
    window.addEventListener('scroll',spy,{passive:true});spy();}
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  }else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});}
})();
