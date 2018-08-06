// Extracting cookies
function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                var cookies = document.cookie.split(";");
                cookies.forEach(function(cookie){
                	cookie = jQuery.trim(cookie);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                });
            }
            return cookieValue;
        }

// Getting data from the search bars
$("#go-btn").click(function() {

	var MeetupLocation = document.getElementById("meetup-location-input").options[document.getElementById("meetup-location-input").selectedIndex].text;
	var SelectedDate = document.getElementById("date-input").value;
	var Keyword = document.getElementById("keyword-input").value;
	var SelectedFilter = document.getElementById("myList").value;
	var Location = document.getElementById("location-input").options[document.getElementById("location-input").selectedIndex].text;
	var csrftoken = getCookie("csrftoken");
	var Data = {
		"csrfmiddlewaretoken": csrftoken,
		"meetup_location": MeetupLocation,
		"date": SelectedDate,
		"keyword": Keyword,
		"filter" : SelectedFilter,
		"location": Location
	};
	$.ajax({
		type: "POST",
		url: "search/",
		data: Data,
		success(a){
			var x = "";
			for(var i of a.search_results){
				x += "<div class=\n" +
				"'text-bottom ml15'>"+i.location +"<div><a href='../"+i.location_slug+"\n" +
				"/"+i.meetup_slug+"''>"+i.meetup+"</a>"+"</div>"+i.date+"\n" +
				"<div><b>"+i.distance+" "+i.unit+"</b></div></div>";			
			}
		$("#meetups-list").html(x);
		},
		dataType:"json",
	});
});

// Hiding the location bar until distance filter is selected
$("#myList").change(function(){
	var SelectedFilter = document.getElementById("myList").value;
	// If date filter is selected
	if(SelectedFilter === "1"){
		$("#location").addClass("hidden");
	}else{
		$("#location").removeClass("hidden");
	}
});
