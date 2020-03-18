// Altered content for the form loaded by crispy forms
var htmlInnerContent="<label for='id_profile_picture' \n" +
"class='control-label'>Profile picture</label><br>\n" +
"<button id='upload_pic' class='btn btn-default' type='button'>\n" +
"UPLOAD PICTURE</button><strong id='file_name_display'>\n" +
 "</strong><div class='controls'> <input name='profile_picture'\n" +
  "class='clearablefileinput' id='id_profile_picture' type='file'\n" +
   "style='position:absolute; left:-999px;'></div>";

// Changing the content of the required div containing photo upload field rendered by crispy forms
$("#div_id_profile_picture").html(htmlInnerContent);

// When custom button is clicked, perform a click on file upload field
$("#upload_pic").click(function() {
	$("#id_profile_picture").click();
});

// When file has been selected, this call back is triggered
document.getElementById("id_profile_picture").onchange = function () {
  var str = this.value;
  // Split the path of file uploaded
  var pathTokens = str.split("\\");
  // Display name of file beside the custom button
  $("#file_name_display").html(" " + pathTokens[pathTokens.length - 1]);
};
