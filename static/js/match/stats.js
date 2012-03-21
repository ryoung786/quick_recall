(function($, _) {
     Stats = function() {
         this.pie_options = {
             series: {
                 pie: {
                     show: true,
                     // innerRadius: .2
                 }
             },
             // legend: { show: false }
         };

         this.tags_options = {
             series: {
                 bars: {
                     show: true,
                     barWidth: 20,
                     align: 'center'
                 },
                 stack: true
             },
             xaxis: {
                 // ticks: [[100, 'math'], [200, 'history'], [300, 'science']],
                 min: 50,
                 max: 350
             }
         };

         this.drawPlayerCorrectIncorrect();
         this.drawTagsBreakdown();
     };

     Stats.prototype = {
         drawPlayerCorrectIncorrect : function() {
             var self = this;
             $('.player').each(function() {
                 var num_correct = $(this).data('num-correct');
                 var num_incorrect = $(this).data('num-incorrect');

                 var data = [{ label: "Correct", data: num_correct },
                             { label: "Incorrect", data: num_incorrect }];
                 $.plot($('.flot.pie', this), data, self.pie_options);
             });
         },
         drawTagsBreakdown : function() {
             var self = this;
             $('.player').each(function() {
                 var correct = $('.correct td', this).map(function() {
                     var x = parseInt($(this).data('xval'));
                     var y = parseInt($(this).text());
                     return [[x, y]];
                 });
                 var incorrect = $('.incorrect td', this).map(function() {
                     var x = parseInt($(this).data('xval'));
                     var y = parseInt($(this).text());
                     return [[x, y]];
                 });

                 var data = [{ label: "Correct", data: correct },
                             { label: "Incorrect", data: incorrect }];
                 console.log(data)

                 var xticks = $('.tag-to-xtick-mapping li', this).map(function() {
                     var xtick = parseInt($(this).text());
                     var tag = $(this).data('tagname');
                     return [[xtick, tag]];
                 });

                 self.tags_options['xaxis']['ticks'] = xticks;
                 $.plot($('.flot.tags', this), data, self.tags_options);
             });
         }
     };
     var stats = new Stats();
}(jQuery, _));
