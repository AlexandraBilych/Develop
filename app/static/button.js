$(document).ready(function(){  

    $("#Rem").click(function ()
      {
         alert('Your book is overdue');
         ShowDialog();
         CreateHTML1();
         CreateHTML2();
      });

      
    $('#btnClose').click(function()
      {
         HideDialog();
      });

    $('input:radio').click(function(){

             if($('input:radio[name=brand]:checked').val() == 'book'){
             $("#booselect").show();
             $("#aselect").hide();
             }
             else{
             $("#booselect").show();
             $("#aselect").hide();
             }

             });
    
     $("#btnSubmit").click(function ()
      {
         var radio = $('input:radio[name=brand]:checked').val();
         var brand = $("#myselect :selected").text();
         $("h3").html("<b>Your select: </b>" + brand + radio);
         HideDialog();
      });


    $(":input").keypress(function() {
        $.ajax({
               url: "/main",
               success: function(data){
               $("#remove_name").empty();
               alert( "Прибыли данные: " + data );
                }
               });






    });


    function ShowDialog(){
        $("#background").show();
        $("#Window_rem").fadeIn(300);
        $("#background").unbind("click");
        }
        
    function HideDialog(){
        $("#background").hide();
        $("#Window_rem").fadeOut(300);
        }

    function CreateHTML2(){
    var data = [{'1':'J. K. Rowling'}, {'2': 'Barbara Park'}, {'3': 'Robert Jordan'}];
    var $select = $('#aselect');
        $.each(data, function(i, val){
        $select.append($('<option />', { value: (i+1), text: val[i+1] }));
        });
    }

    function CreateHTML1(){
    var data = [{'1':'Harry Potter and the Chamber of Secrets'}, {'2': 'The Wheel of Time'}, {'3': 'The Alchemist'}];
    var $select = $('#booselect');
        $.each(data, function(i, val){
        $select.append($('<option />', { value: (i+1), text: val[i+1] }));
        });
    }