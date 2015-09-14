$(document).ready(function(){

    $("#Add").click(function (e)
      {
         ShowDialog(true);
         e.preventDefault();
      });

    $("#btnSubmit").click(function (e)
      {
         var add = $("#brands input:radio:checked").val();
         $("#output").html("<b>You chose: </b>" + add);
         HideDialog();
         e.preventDefault();
      });

    $("#content").mouseover(function(){
        alert("1. Editing 2. Remove");
                                       });

    $("name").mouseover(function(){
        $(this).css("text-decoration", "underline");
        $(this).css("color","red");
                                 });

    $("name").mouseout(function(){
        $(this).css("text-decoration", "none");
        $(this).css("color","black");
                                 });


                           });

    function ShowDialog(modal)
    {
      $("#overlay").show();
      $("#dialog").fadeIn(300);

      if (modal)
      {
         $("#overlay").unbind("click");
      }
      else
      {
         $("#overlay").click(function (e)
         {
            HideDialog();
         });
      }
   }

     function HideDialog()
   {
      $("#dialog").hide();
      $("#overlay").fadeOut(300);
   }
