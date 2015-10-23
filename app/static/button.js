$(document).ready(function(){
      jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
      });

      jQuery.validator.addMethod("thesame", function(value, element) {
	   return this.optional(element) || value != $('#list option:selected').text();
      }, "The name doesn't change!")

      jQuery.validator.addMethod("exist", function(value, element) {
      if($(".criteria input[type=radio]:checked").val() == "value_book"){
        $.ajax({
        type: 'POST',
        url: '/GetBookList',
        async: false,
        success: function(books){
        mas = JSON.parse(books);
        ex = true;
        for(var i = 0; i < mas.length; i++){
            if ($('input[id="edit_name"]').val()==mas[i].name){
                ex = false;
                }
        }
        }
       });
       }
       else{
       $.ajax({
        type: 'POST',
        url: '/GetAuthorList',
        async: false,
        success: function(authors){
        mas = JSON.parse(authors);
        ex = true;
        for(var i = 0; i < mas.length; i++){
            if ($('input[id="edit_name"]').val()==mas[i].name){
                ex = false;
                }
        }
        }
       });
       }
       return ex;

      }, "This name has already existed!");



      jQuery.validator.addMethod("present", function(value, element) {
      alert($("#rem_criterion input[type=radio]:checked").val());
      if($("#rem_criterion input[type=radio]:checked").val() == "value_book"){
        $.ajax({
        type: 'POST',
        url: '/GetBookList',
        async: false,
        success: function(books){
        mas = JSON.parse(books);
        ex = false;
        for(var i = 0; i < mas.length; i++){
            if ($('input[id="RemoveForm.rem_name"]').val()==mas[i].name){
                ex = true;
                }
        }
        }
       });
       }
       else{
       $.ajax({
        type: 'POST',
        url: '/GetAuthorList',
        async: false,
        success: function(authors){
        mas = JSON.parse(authors);
        ex = false;
        for(var i = 0; i < mas.length; i++){
            if ($('input[id="RemoveForm.rem_name"]').val()==mas[i].name){
                ex = true;
                }
        }
        }
       });
       }
       return ex;

      }, "This book/author isn't in the library!");



    $.ajax({
        type: 'POST',
        url: '/GetBookList',
        success: function(books){
        mas = JSON.parse(books);
            for(var i = 0; i < mas.length; i++){
                $('#searchlist').append("<option value=\"" + mas[i].name + "\">");
                $('#removelist').append("<option value=\"" + mas[i].name + "\">");
            }
        }
    });

    $("#criterion").change(function ()
    {$('#searchlist').children().remove();

     if($("#criterion input[type=radio]:checked").val() == "value_author")
         {CreateDatalistAuthor();}
     else {CreateDatalistBook();}

     });

    $("#rem_criterion").change(function ()
    {$('#removelist').children().remove();

     if($("#rem_criterion input[type=radio]:checked").val() == "value_author")
         {CreateDatalistAuthor();}
     else {CreateDatalistBook();}

     });


    $(".popup").click(function ()
      {
         var id = this.id
         ShowDialog(id);
         CreateHTML1();
      });

    $("#Reset").click(function ()
      {
          $("#EditForm").validate().resetForm();
          $('input[id="edit_name"]').attr('value','');
      });


    $('#list').change(function()
      {
         var text = $('#list option:selected').text();
         $('input[id="edit_name"]').attr('value',text);
         $('input[id="edit_name"]').css("width", $('#list').css('width'));
      });


    $(".criteria input[type=radio]").change(function()
      {
      $('#list').children().remove();
      $('input[id="edit_name"]').attr('value','');
      if($(".criteria input[type=radio]:checked").val() == "value_author"){
      CreateHTML2();}
      else {CreateHTML1();}
     });


    $('.btnClose').click(function()
      {
         var id = this.id
         HideDialog(id);
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
   if (id == "Rem"){ $("#Window_rem").fadeIn(300);}
   else if (id == "Edit"){ $("#Window_edit").fadeIn(300);}
   $("#background").unbind("click");
}
        
function HideDialog(id){
   $("#background").hide();
   if (id == "btnClose11"){ $("#Window_rem").fadeOut(300);}
   else if (id == "btnClose12"){ $("#Window_edit").fadeOut(300);}
 }

function CreateHTML1(){
    $.ajax({
        type: 'POST',
        url: '/GetBookList',
        success: function(books){
        mas = JSON.parse(books);
            for(var i = 0; i < mas.length; i++){
                $('#list').append("<option value=\"" + mas[i].id + "\">" + mas[i].name + "</option>");
            }
        }
    });
}

function CreateHTML2(){
    $.ajax({
        type: 'POST',
        url: '/GetAuthorList',
        success: function(authors){
        mas = JSON.parse(authors);
        for(var i = 0; i < mas.length; i++){
            $('#list').append("<option value=\"" + mas[i].id + "\">" + mas[i].name + "</option>");
        }
        }
    });
}

function CreateDatalistBook(){
    $.ajax({
        type: 'POST',
        url: '/GetBookList',
        success: function(books){
        mas = JSON.parse(books);
            for(var i = 0; i < mas.length; i++){
                $('#searchlist').append("<option value=\"" + mas[i].name + "\">");
                $('#removelist').append("<option value=\"" + mas[i].name + "\">");
            }
        }
    });
}

function CreateDatalistAuthor(){
    $.ajax({
        type: 'POST',
        url: '/GetAuthorList',
        success: function(authors){
        mas = JSON.parse(authors);
        for(var i = 0; i < mas.length; i++){
            $('#searchlist').append("<option value=\"" + mas[i].name + "\">");
            $('#removelist').append("<option value=\"" + mas[i].name + "\">");
        }
        }
    });
}