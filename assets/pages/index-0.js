
(function(){
  
  var CAMP=[
    {s:'september',n:'Crisis Prevention & DV Awareness',d:'September – October',m:[8,9],c:'#0F6E6E',i:'#0A4A4A'},
    {s:'november',n:'Transgender Awareness & TDOR',d:'November 13–20',m:[10],c:'#3A6EA5',i:'#274B72'},
    {s:'december',n:'Human Rights Day',d:'December 10',m:[11],c:'#0063A6',i:'#004675'},
    {s:'january',n:'Human Trafficking Prevention',d:'January',m:[0],c:'#1E4B8F',i:'#183A6E'},
    {s:'february',n:'Black History Month',d:'February',m:[1],c:'#1B7A3D',i:'#12562B'},
    {s:'march',n:"Women's History & IWD",d:'March',m:[2],c:'#6A1B9A',i:'#551579'},
    {s:'april',n:'SAAM & Fair Housing',d:'April',m:[3],c:'#0F7C7C',i:'#0A5252'}
  ];
  var mo=new Date().getMonth();
  var cur=CAMP.filter(function(c){return c.m.indexOf(mo)>=0;})[0];
  var sp=document.getElementById('spot');
  if(sp){
    var pick=cur||CAMP[0];var tag=cur?'Active campaign this month':'Next campaign up';
    sp.style.setProperty('--accent-strong',pick.c);sp.style.setProperty('--accent-ink',pick.i);
    sp.querySelector('.spot__title').textContent=pick.n;
    sp.querySelector('.spot__meta').textContent=pick.d+(cur?' — happening now':' — the season opener');
    sp.querySelector('.spot__tag-txt').textContent=tag;
    sp.querySelector('.spot__go a').href='campaigns/'+pick.s+'.html';
  }
})();
