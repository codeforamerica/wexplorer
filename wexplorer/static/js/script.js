(function($, window) {
  var t = document.getElementById('js-cycle-phrases');
  var phrases = [
    'for the lowest price.',
    'covered by existing contracts.',
    'from local vendors.',
    'requiring the least paperwork.',
  ];
  var count = 1;
  if (t) {
    setInterval(function(){
      t.innerHTML=phrases[count];
      count++;
      if(count>=phrases.length) {
        count=0;
      }
    }, 1600);
  }

  var searchResults = $('#js-explore-search-results');
  if (searchResults.length > 0) {
    searchResults.find('th').click(function() {
      var _table = $(this).parents('table').eq(0);
      var rows = _table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
      this.asc = !this.asc;
      if (!this.asc) { rows = rows.reverse(); }
      for (var i=0; i<rows.length; i++) {
        _table.append(rows[i]);
      }
    })

    function comparer(index) {
      return function(a,b) {
        var valA = getCellValue(a, index);
        var valB = getCellValue(b, index);
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB);
      }
    }

    function getCellValue(row, index) {
      return $(row).children('td').eq(index).text();
    }

  }
}).call(this, jQuery, window);
