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

             $('input[type="submit"]').click(function() {
                 self.submitForm($(this).parent(), $(this).val());
                 return false;
             });
         },

         submitForm : function(form, submit_btn_val) {
             var data = this.getFormData(form);
             data.correct = (submit_btn_val == 'Correct') ? 1 : 0;
             $.post("questions", data, function(resp) {
                  alert("response: " + resp);
             });
             return false;
         },

         getFormData : function(form) {
             var tags = $(form).siblings('ul.tags');
             var selected = tags.find('.selected');
             var data = {'tags': []}
             $.each($(form).serializeArray(), function(i, field) {
                 data[field.name] = field.value;
             });
             selected.each(function() {
                 data.tags = data.tags.concat($(this).text())
             });
             return data;
         },
     };

     var match = new Match();
}(jQuery, _));
