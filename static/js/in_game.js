(function($, _) {
     Game = function() {
         this.bindHandlers();
     };

     Game.prototype = {
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
				 console.log(selected);
				 selected.each(function() {
					 console.log($(this).text());
					 $(form).append('<input type="hidden" name="tags" value="' + $(this).text() + '">');
				 });
				 return true;
			 });
         }
     };

     var game = new Game();
}(jQuery, _));
