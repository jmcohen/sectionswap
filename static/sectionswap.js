var setSectionOptions = function(sections){
// 	var height = $("#container").height();
// 	$("#container").height(height);

	$("#submit").show();
	$("#have-label").show();
	$("#have-options").empty();
	_.each(sections, function(section){
		$("#have-options").append('<label class="radio"><input name="have" class="have-option" value="' + section.number + '" type="radio">' + section.name + '</label>');
	});
	$("#want-label").show();
	$("#want-options").empty();
	_.each(sections, function(section){
		$("#want-options").append('<label class="checkbox"><input name="want" class="want-option" value="' + section.number + '" type="checkbox">' + section.name + '</label>');
	});
	
	$("body").attr("background", "-webkit-linear-gradient(#FFFFFF, #EEEEEE)");
	var width = $("#want-options").width();
	$("#options-div").width(40 + width * 2);
	
// 	$('#container').css('height', 'auto');
// 	var autoHeight = $('#container').height();
// 	$('#container').height(height).animate({height: autoHeight}, 300);
}


// Random background image
var images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg'];
$('body').css({'background-image': 'url(static/bg_orange/' + images[Math.floor(Math.random() * images.length)] + ')'});


// Executed on document load 
$(document).ready(function(){

	$.getJSON("courses", function(courses){
		_.each(courses, function(course){
			var el = $('<option value="' + course['number'] + '"></option>').text(course['code']);
			$("#section-select").append(el);
		});
		
	$("#section-select").change(function(){
		var selectedNumber = $("#section-select").val();
		var selectedCourse = _.find(courses, function(course){return selectedNumber == course.number;});
		setSectionOptions(selectedCourse.sections);
	});
});


	$("#submit").click(function(){
		var courseNumber = $("#section-select").val();	
		var haveNumber = $(".have-option:checked").val();
		var wantNumber = _.map($(".want-option:checked"), function(w){return $(w).val()});
		var user = "jmcohen";
		var url = "swaprequest?course=" + courseNumber + "&have=" + haveNumber + "&want=" + wantNumber + "&user=" + user;
		window.location.href = url;
	});
});
