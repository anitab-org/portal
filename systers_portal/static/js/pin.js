function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		cookies.forEach(function(cookie){
			cookie = jQuery.trim(cookie);
                    // Does this cookie string begin with the name we want?
                    inner:if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    	break inner;
                    }
                });
	}
	return cookieValue;
}
$("#pin").click(function() {
	let csrftoken = getCookie("csrftoken")
	let Data = {
		"csrfmiddlewaretoken": csrftoken,
	};
	$.ajax({
		type: "POST",
		url: "pin/",
		data: Data,
		success(a){
			$("#pin").hide();
	    $("#remove").show();
		},
		dataType:"json",
	});
});

$("#remove").click(function() {
	let csrftoken = getCookie("csrftoken")
	let Data = {
		"csrfmiddlewaretoken": csrftoken,
	};
	$.ajax({
		type: "POST",
		url: "unpin/",
		data: Data,
		success(a){
      $("#remove").hide();
	    $("#pin").show();
		},
		dataType:"json",
	});
});

$(function(){
$(".unpin").click(function(){
let id = this.id;
let s = ".blog-entry" + "." + id;

let csrftoken = getCookie("csrftoken")
let Data = {
    "id": id,
		"csrfmiddlewaretoken": csrftoken,
	};
	$.ajax({
		type: "POST",
		url: "unpin/",
		data: Data,
		success(a){
		  $(s).hide();
		},
		dataType:"json",
		});
});
});
