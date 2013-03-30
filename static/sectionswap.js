var setSectionOptions = function(sections){
// 	var height = $("#container").height();
// 	$("#container").height(height);
	$("#submit").show();
	$("#have-label").show();
	$("#have-options").empty();
	_.each(sections, function(section){
		var el = $('<label class="radio"><input name="have" class="have-option" value="' + section.number + '" type="radio">' + section.name + '</label>');
		$("#have-options").append(el);
	});
	$("#want-label").show();
	$("#want-options").empty();
	_.each(sections, function(section){
		var el = $('<label class="checkbox"><input name="want" class="want-option" ' + ' value="' + section.number + '" type="checkbox">' + section.name + '</label>');
		$("#want-options").append(el);
		el.attr('disabled', 'true');
	});
	
	$("body").attr("background", "-webkit-linear-gradient(#FFFFFF, #EEEEEE)");
	var width = $("#want-options").width();
	$("#options-div").width(60 + width * 2);
	
// 	$('#container').css('height', 'auto');
// 	var autoHeight = $('#container').height();
// 	$('#container').height(height).animate({height: autoHeight}, 300);
}

function get_user_query() {
    name = 'netid';
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if(results == null)
	return "";
    else
	return decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Random background image selection
bg = $('#randbg')
bg.randomImage();
bg.load(function() {
    bg.fadeIn(1000);
});

// Executed on document load 
$(document).ready(function(){
    
    $('#container').fadeIn();
    
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
	var user = get_user_query();
	user = user == "" ? 'jmcohen' : user;
	var url = "swaprequest?course=" + courseNumber + "&have=" + haveNumber + "&want=" + wantNumber + "&user=" + user;
	window.location.href = url;
    });
    
    $("#section-select").select2();
});
