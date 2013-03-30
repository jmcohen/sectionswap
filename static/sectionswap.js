var setSectionOptions = function(sections){
	$("#have-options").empty();
	_.each(sections, function(section){
		$("#have-options").append('<label class="radio"><input name="have" class="have-option" value="' + section.number + '" type="radio">' + section.name + '</label>');
	});
	$("#want-options").empty();
	_.each(sections, function(section){
		$("#want-options").append('<label class="checkbox"><input name="want" class="want-option" value="' + section.number + '" type="checkbox">' + section.name + '</label>');
	});
}

$(document).ready(function(){
	$.getJSON("courses", function(courses){
		_.each(courses, function(course){
			$("#section-select").append('<option value="' + course['number'] + '">' + course['code'] + '</option>');
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
		var url = "swaprequest?course=" + courseNumber + "&have=" + haveNumber + "&want=" + wantNumber;
		window.location.href = url;
	});
});