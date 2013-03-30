var courses = {
	"COS 126": ["P01 (MWF 10:00 - 11:00)", "P02 (MWF 10:00 - 11:00)", "P03 (MWF 10:00 - 11:00)","P04 (MWF 10:00 - 11:00)"],
	"COS 226": ["L01 (MWF 10:00 - 11:00)", "L02 (MWF 10:00 - 11:00)", "L03 (MWF 10:00 - 11:00)","L04 (MWF 10:00 - 11:00)"]
};

var setSelectedCourse = function(course){
	var sections = courses[course];
	$("#have-options").empty();
	_.each(sections, function(section, index){
		$("#have-options").append('<label class="radio"><input name="have" value="' + index + '" type="radio">' + section + '</label>');
	});
	$("#want-options").empty();
	_.each(sections, function(section, index){
		$("#want-options").append('<label class="checkbox"><input name="want" value="' + index + '" type="checkbox">' + section + '</label>');
	});
}

$(document).ready(function(){
	_.each(_.keys(courses), function(key){
		console.log(key);
		$("#section-select").append('<option>' + key + '</option>');
	});

	$("#section-select").change(function(){
		var selected = $("#section-select").val();
		setSelectedCourse(selected);
	});
	
	setSelectedCourse("COS 126");
});