$(document).ready(function(){
      var book_array = [];
      var author_array = [];

      $.ajax({
        type: 'POST',
        url: '/GetAuthorList',
        async: false,
        success: function(authors){
        author_array = JSON.parse(authors);
        }
      });

      $.ajax({
        type: 'POST',
        url: '/GetBookList',
        async: false,
        success: function(books){
        book_array = JSON.parse(books);
        }
      });

/* fills values to search for */
    for(var i = 0; i < book_array.length; i++){
        $('#searchlist').append("<option value=\"" + book_array[i].name + "\">");
        $('#removelist').append("<option value=\"" + book_array[i].name + "\">");
        $('#list').append("<option value=\"" + book_array[i].id + "\">" + book_array[i].name + "</option>");
    }

/* Validation input fields START */
      jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
      });


      jQuery.validator.addMethod("thesame", function(value, element) {
	   return this.optional(element) || value != $('#list option:selected').text();
      }, "The name doesn't change!")


      jQuery.validator.addMethod("exist", function(value, element) {
      if($(".criteria input[type=radio]:checked").val() == "value_book"){
        ex = true;
        for(var i = 0; i < book_array.length; i++){
            if ($('input[id="edit_name"]').val()==book_array[i].name){
                ex = false;
            }
       }
      }
      else{
          ex = true;
          for(var i = 0; i < author_array.length; i++){
              if ($('input[id="edit_name"]').val()==author_array[i].name){
                  ex = false;
              }
          }
       }
      return ex;

      }, "This name has already existed!");


      jQuery.validator.addMethod("present", function(value, element) {
      alert($("#rem_criterion input[type=radio]:checked").val());
      if($("#rem_criterion input[type=radio]:checked").val() == "value_book"){
        ex = false;
        for(var i = 0; i < book_array.length; i++){
            if ($('input[id="RemoveForm.rem_name"]').val()==book_array[i].name){
                ex = true;
            }
       }
      }
      else{
          ex = false;
          for(var i = 0; i < author_array.length; i++){
              if ($('input[id="RemoveForm.rem_name"]').val()==author_array[i].name){
                  ex = true;
              }
          }
      }
      return ex;

      }, "This book/author isn't in the library!");
/* Validation input fields END */


    $("#criterion").change(function (){
        if($("#criterion input[type=radio]:checked").val() == "value_author"){
            CreateDatalist(author_array, 'searchlist' );
        }
        else {
            CreateDatalist(book_array, 'searchlist');
        }
    });


    $("#rem_criterion").change(function (){
        if($("#rem_criterion input[type=radio]:checked").val() == "value_author"){
            CreateDatalist(author_array, 'removelist');
        }
        else {
            CreateDatalist(book_array, 'removelist');
        }
    });


    $(".popup").click(function (){
        var id = this.id
        ShowDialog(id);
       if (id == "Add_author"){
           CreateDatalist(author_array, 'authorlist');
           CreateDatalist(book_array, 'books');
       }
       else if (id == "Add_book"){
           CreateDatalist(book_array, 'booklist');
           CreateDatalist(author_array, 'authors');
       }
       else if (id == "Edit"){
           /*CreateHTML(book_array, 'list');*/
       }
    });


    $('.btnClose').click(function()
      {
         var id = this.id
         HideDialog(id);
      });


    $("#Reset").click(function (){
        $("#EditForm").validate().resetForm();
        $('input[id="edit_name"]').attr('value','');
        $("#list").children().remove();
        CreateHTML(book_array, 'list');
    });


    $('#list').change(function(){
        var text = $('#list option:selected').text();
        $('input[id="edit_name"]').attr('value',text);
        $('input[id="edit_name"]').css("width", $('#list').css('width'));
    });


    $(".criteria input[type=radio]").change(function(){
        $('input[id="edit_name"]').attr('value','');
        $("#list").children().remove();
        if($(".criteria input[type=radio]:checked").val() == "value_author"){
            CreateHTML(author_array, 'list');
        }
        else {
            CreateHTML(book_array, 'list');
        }
     });


    $('#EditForm').validate({
    rules: {
      edit_name: {
         required: true,
         thesame: true,
         exist: true
      }
    },
    submitHandler: function(form) {
        form.submit();
    }
});


});



function ShowDialog(id){
   $("#background").show();
   if (id == "Rem"){
       $("#Window_rem").fadeIn(300);
   }
   else if (id == "Edit"){
       $("#Window_edit").fadeIn(300);
   }
   else if (id == "Add_author"){
       $("#Window_aadd").fadeIn(300);
   }
   else if (id == "Add_book"){
       $("#Window_badd").fadeIn(300);
   }
   $("#background").unbind("click");
}


function HideDialog(id){
   $("#background").hide();
   if (id == "btnClose1"){
       $("#Window_rem").fadeOut(300);
   }
   else if (id == "btnClose2"){
       $("#Window_edit").fadeOut(300);
   }
   else if (id == "btnClose4"){
       $("#Window_aadd").fadeOut(300);
   }
   else if (id == "btnClose6"){
       $("#Window_badd").fadeOut(300);
   }
 }


function CreateHTML(array, id){
    $('#' + id + ' option:gt(0)').remove().end();
    for(var i = 0; i < array.length; i++){
        $('#' + id).append("<option value=\"" + array[i].id + "\">" + array[i].name + "</option>");
    }
}


function CreateDatalist(array, id){
    $('#' + id).children().remove();
    for(var i = 0; i < array.length; i++){
        $('#' + id).append("<option value=\"" + array[i].name + "\">");
    }
}