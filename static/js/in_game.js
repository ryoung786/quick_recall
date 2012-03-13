(function($, _) {
     Match = function() {
         // TODO keep track of the current question (or lack
         //      thereof so we can modify the form post action
         this.bindHandlers();
     };

     Match.prototype = {
         bindHandlers : function() {
             var self = this;

             $('.avatar').click(function() {
				 var question = $(this).siblings('.question');
				 question.toggle();
             });

			 $('.tags li').click(function() {
				 $(this).toggleClass('selected');
			 });

			 $('form').submit(function() {
				 var form = this;
				 var tags = $(this).siblings('ul.tags');
				 var selected = tags.find('.selected');
				 selected.each(function() {
					 $(form).append('<input type="hidden" name="tags" value="' + $(this).text() + '">');
				 });
				 return true;
			 });
         }
     };

     var match = new Match();
}(jQuery, _));
