(function () {
  var campaigns = [
    { slug: 'september', name: 'Crisis Prevention & DV Awareness', dates: 'September – October', months: [8, 9] },
    { slug: 'november', name: 'Transgender Awareness & TDOR', dates: 'November 13–20', months: [10] },
    { slug: 'december', name: 'Human Rights Day', dates: 'December 10', months: [11] },
    { slug: 'january', name: 'Human Trafficking Prevention', dates: 'January', months: [0] },
    { slug: 'february', name: 'Black History Month', dates: 'February', months: [1] },
    { slug: 'march', name: "Women's History & IWD", dates: 'March', months: [2] },
    { slug: 'april', name: 'SAAM & Fair Housing', dates: 'April', months: [3] }
  ];
  var month = new Date().getMonth();
  var current = campaigns.filter(function (campaign) { return campaign.months.indexOf(month) >= 0; })[0];
  var spotlight = document.getElementById('spot');
  if (!spotlight) return;
  var pick = current || campaigns[0];
  spotlight.classList.add('spot--' + pick.slug);
  spotlight.querySelector('.spot__title').textContent = pick.name;
  spotlight.querySelector('.spot__meta').textContent = pick.dates + (current ? ' — happening now' : ' — the season opener');
  spotlight.querySelector('.spot__tag-txt').textContent = current ? 'Active campaign this month' : 'Next campaign up';
  spotlight.querySelector('.spot__go a').href = 'campaigns/' + pick.slug + '.html';
})();
