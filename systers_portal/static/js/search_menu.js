// Getting data from the search bars
$("#go-btn").click(function() {

	var MeetupLocation = document.getElementById("meetup-location-input").options[document.getElementById("meetup-location-input").selectedIndex].text;
	var SelectedDate = document.getElementById("date-input").value;
	var Keyword = document.getElementById("keyword-input").value;
	var SelectedFilter = document.getElementById("myList").value;
	var Location = document.getElementById("location-input").options[document.getElementById("location-input").selectedIndex].text;

	var Data = {
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
			var x = document.getElementById("meetups-list");
			x.innerHTML = "";
			for(var i of a.search_results){
				x.innerHTML += "<div class=\n" +
				"'text-bottom ml15'>"+i.location +"<div><a href='../"+i.location_slug+"\n" +
				"/"+i.meetup_slug+"''>"+i.meetup+"</a>"+"</div>"+i.date+"\n" +
				"<div><b>"+i.distance+" "+i.unit+"</b></div>";			
			}
		},
		dataType:"json",
		error(e){
			alert(e);
		}
	});
});

// Hiding the location bar until distance filter is selected
$("#myList").change(function(){
	var SelectedFilter = document.getElementById("myList").value;
	if(SelectedFilter === "1"){
		$("#location").addClass("hidden");
	}else{
		$("#location").removeClass("hidden");
	}
});
