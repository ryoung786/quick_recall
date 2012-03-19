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
         this.drawPlayerCorrectIncorrect();
     };

     Stats.prototype = {
         drawPlayerCorrectIncorrect : function() {
             var self = this;
             $('.player').each(function() {
                 var num_correct = $(this).data('num-correct');
                 var num_incorrect = $(this).data('num-incorrect');
                 var data = [num_correct, num_incorrect];

                 var data = [{ label: "Correct", data: num_correct },
                             { label: "Incorrect", data: num_incorrect }];
                 $.plot($('.flot', this), data, self.pie_options);
             });
         }
     };
     var stats = new Stats();
}(jQuery, _));
