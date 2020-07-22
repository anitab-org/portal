// Extracting cookies to pass the csrf token authentication
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

// Getting data from the search bars
$("#go-btn").click(function() {

	let Keyword = document.getElementById("keyword-input").value;
	let Location = document.getElementById("location").options[document.getElementById("location").selectedIndex].text;
	let csrftoken = getCookie("csrftoken");
	let Data = {
	  "csrfmiddlewaretoken": csrftoken,
		"keyword": Keyword,
		"location": Location
	};
	$.ajax({
		type: "POST",
		url: "search/",
		data: Data,
		success(a){
		let x="";
		  if(a.search_results.length==0){
		     x = `<h3>No Meetups Found</h3>`;
		  }
			else{
			   x = `<div class="row">`;
			for(var i of a.search_results){
			  let link = `../${i.meetup_slug}/`;
			  x = x + `<div class="col-sm-6 col-md-4">
			             <div class="thumbnail">
			                  <div class="caption">
			                     <h3> ${i.meetup} </h3>
			                      <h4> ${i.date}  </h4>
			                      <h5> ${i.location} </h5>
			                      <h5> ${i.distance}  ${a.unit} </h5>
			                      <p align="right">
			                        <a href=${link} class="btn btn-primary" role="button">Checkout</a>
			                      </p>
			                  </div>
			             </div>
			            </div>`;
			}
			x = x + `</div>`;
			}
		$("#meetups-list").html(x);
		},
		dataType:"json",
	});
});
