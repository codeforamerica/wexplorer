(function($, window) {
  var t = document.getElementById('js-cycle-phrases');
  var phrases = [
    'for the lowest price',
    'covered by existing contracts',
    'from local vendors',
    'requiring the least paperwork',
  ];
  var count = 1;
  setInterval(function(){
    t.innerHTML=phrases[count];
    count++;
    if(count>=phrases.length) {
      count=0;
    }
  }, 1600);
}).call(this, jQuery, window);
