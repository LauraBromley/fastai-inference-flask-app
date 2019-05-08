function readURL(input) {

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#chosen-image').attr('src', e.target.result);
      $("#step-1").hide();
      $("#step-2").show();
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$( document ).ready(function() {

  $("#image-file").change(function() {
    readURL(this);
  });

  $("#step-1").show();
  $("#step-2").hide();

});