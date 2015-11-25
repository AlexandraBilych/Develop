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
	  
	  
	jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
      });
	  
/* Presetting forms */	  
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
           CreateHTML(book_array, 'list');
		   $('input[id="edit_name"]').attr('value', $('#list option:selected').text());
		   $('#Alist').empty();		
		   $.ajax({
                type: 'POST',
                data: JSON.stringify({edit_name: $('#list option:selected').text()}),
                url: '/GetAutorsforBook',
                async: false,
                success: function(data){
                authors = JSON.parse(data);
                }
           });
           for(var i = 0; i < authors[0].name.length; i++){
           $('#Alist').append("<input name=\"first\" type=\"checkbox\" value=\"" + authors[0].name[i] + "\" checked>" + authors[0].name[i] + "<br>");
           }
           }
    });


    $('.btnClose').click(function()
      {
         var id = this.id
         HideDialog(id);
    });
	  
	
/* fills values to search for */
    for(var i = 0; i < book_array.length; i++){
        $('#searchlist').append("<option value=\"" + book_array[i].name + "\">");
        $('#removelist').append("<option value=\"" + book_array[i].name + "\">");
      /*  $('#list').append("<option value=\"" + book_array[i].id + "\">" + book_array[i].name + "</option>");*/
    }	
	  
/* SEARCH */
/* Add attribute "list" for input field Searchform */

    var s = document.getElementById("search");
    var att1 = document.createAttribute("list");
    att1.value = "searchlist";
    s.setAttributeNode(att1);
    s.required = true;
	
	
    $("#criterion").change(function (){
        if($("#criterion input[type=radio]:checked").val() == "value_author"){
            CreateDatalist(author_array, 'searchlist' );
        }
        else {
            CreateDatalist(book_array, 'searchlist');
        }
    });
	
	

/* REMOVE */
/* Add attribute "list" for input field Searchform */

    var r = document.getElementById("rem_name");
    var att2 = document.createAttribute("list");
    att2.value = "removelist";
    r.setAttributeNode(att2);
    r.required = true;
	
	
/* Validation input fields */
    jQuery.validator.addMethod("present", function(value, element) {
      alert($("#rem_criterion input[type=radio]:checked").val());
      if($("#rem_criterion input[type=radio]:checked").val() == "value_book"){
        ex = false;
        for(var i = 0; i < book_array.length; i++){
            if ($('input[id="rem_name"]').val()==book_array[i].name){
                ex = true;
            }
       }
      }
      else{
          ex = false;
          for(var i = 0; i < author_array.length; i++){
              if ($('input[id="rem_name"]').val()==author_array[i].name){
                  ex = true;
              }
          }
      }
      return ex;

      }, "This book/author isn't in the library!");

	
    $("#rem_criterion").change(function (){
        if($("#rem_criterion input[type=radio]:checked").val() == "value_author"){
            CreateDatalist(author_array, 'removelist');
        }
        else {
            CreateDatalist(book_array, 'removelist');
        }
    });
	
	
/* Validation with custom method
  $('#RemoveForm').validate({
    rules: {
      rem_name: {
         present: true
      }
    },
    submitHandler: function(form) {
        form.submit();
    }
    }); */
	
	
/* EDIT */
/* Validation input fields */
    jQuery.validator.addMethod("thesame", function(value, element) {
        return this.optional(element) || value != $('#list option:selected').text();
        }, "The name doesn't change!")
		
		
	jQuery.validator.addMethod("exist", function(value, element) {
      if($(".criteria input[type=radio]:checked").val() == "value_book"){
        ex = true;
        for(var i = 0; i < book_array.length; i++){
            if (book_array[i].name != $('#list option:selected').text()){
                if ($('input[id="edit_name"]').val()==book_array[i].name){
                    ex = false;
                }
            }
       }
      }
      else{
          ex = true;
          for(var i = 0; i < author_array.length; i++){
              if (author_array[i].name != $('#list option:selected').text()){
              if ($('input[id="edit_name"]').val()==author_array[i].name){
                  ex = false;
              }
              }

          }
       }
      return ex;

      }, "This name has already existed!");

	
    $("#Reset").click(function (){
        $("#EditForm").validate().resetForm();
		$("#list").children().remove();
		CreateHTML(book_array, 'list');
        $('input[id="edit_name"]').attr('value', $('#list option:selected').text());
        $('#Alist').empty();		
		$.ajax({
                type: 'POST',
                data: JSON.stringify({edit_name: $('#list option:selected').text()}),
                url: '/GetAutorsforBook',
                async: false,
                success: function(data){
                authors = JSON.parse(data);
                }
        });
        for(var i = 0; i < authors[0].name.length; i++){
            $('#Alist').append("<input name=\"first\" type=\"checkbox\" value=\"" + authors[0].name[i] + "\" checked>" + authors[0].name[i] + "<br>");
        }
    });	
	  
	  
    $(".criteria input[type=radio]").change(function(){
        $('input[id="edit_name"]').attr('value','');
        $("#list").children().remove();
		$('#Alist').empty();
        if($(".criteria input[type=radio]:checked").val() == "value_author"){
            CreateHTML(author_array, 'list');
        }
        else {

            CreateHTML(book_array, 'list');

        }
    });
	 
	
    $('#list').click(function(){
        var text = $('#list option:selected').text();
        $('input[id="edit_name"]').attr('value',text);
        $('input[id="edit_name"]').css("width", $('#list').css('width'));
		$('#Alist').empty();
		if (($(".criteria input[type=radio]:checked").val() == "value_book")){
		    $.ajax({
                type: 'POST',
                data: JSON.stringify({edit_name: text}),
                url: '/GetAutorsforBook',
                async: false,
                success: function(data){
                authors = JSON.parse(data);
                }
            });
            for(var i = 0; i < authors[0].name.length; i++){
                $('#Alist').append("<input name=\"first\" type=\"checkbox\" value=\"" + authors[0].name[i] + "\" checked>" + authors[0].name[i] + "<br>");
            }
		    }
		else{
		    $.ajax({
                type: 'POST',
                data: JSON.stringify({edit_name: text}),
                url: '/GetBooksforAuthor',
                async: false,
                success: function(data){
                books = JSON.parse(data);
                }
            });
            for(var i = 0; i < books[0].name.length; i++){
                $('#Alist').append("<input name=\"first\" type=\"checkbox\" value=\"" + books[0].name[i] + "\" checked>" + books[0].name[i] + "<br>");
            }
		}


    });

	
    $('#EditForm').validate({
    rules: {
      edit_name: {
         required: true,
         exist: true
      }
    },
    submitHandler: function(form) {
        form.submit();
    }
    });


	  
/* AADD */



/* BADD */ 


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
 $('#list').append("<option value=\"" + book_array[i].id + "\">" + book_array[i].name + "</option>");

function CreateDatalist(array, id){
    $('#' + id).children().remove();
    for(var i = 0; i < array.length; i++){
        $('#' + id).append("<option value=\"" + array[i].name + "\">");
    }
}
