function toggle_course (course_div)
{
	var opened = course_div.attr('data-course-opened');
	
	if (opened == 0) {
		open_course(course_div);
		course_div.attr('data-course-opened', 1);
	}
	else {
		close_course(course_div);
		course_div.attr('data-course-opened', 0);
	}
}


function open_course (course_div)
{
	var course_id = course_div.attr('data-course-id');
	
	var do_open = function () {
		$('.course-ratings', course_div).slideDown();
		$('.course-name-icon', course_div).removeClass('icon-chevron-down').addClass('icon-chevron-up');
	}
	
	// load ratings if necessary
	if (course_div.attr('data-course-ratings-loaded') == 0) {
		load_course_ratings(course_div, do_open); // load and then animate
	}
	else {
		do_open(); // animate
	}
}


function close_course (course_div)
{
	var course_id = course_div.attr('data-course-id');
	
	$('.course-ratings', course_div).slideUp();
	$('.course-name-icon', course_div).removeClass('icon-chevron-up').addClass('icon-chevron-down');
}


function load_course_ratings (course_div, callback)
{
	var course_id = course_div.attr('data-course-id');
	
	/* loading ... */
	
	$.getJSON('/api/ratings?course_id='+course_id, null, function (data) {
		
		// prepare and append markup for each rating
		for (i in data.ratings) {
			
			var rating = data.ratings[i];
			rating.remark = rating.remark.replace(/\n/, '<br />');
			var markup = $.nano($('#tpl-course-rating').html(), rating);
			
			$('.course-ratings', course_div).prepend(markup);
		}
		
		// if provided, call the callback function after 5ms to let the
		// browser compute the new size of the course-ratings div
		if (callback) setTimeout(callback, 5);
		
		// set the course_div status as 'loaded'
		course_div.attr('data-course-ratings-loaded', 1); // set as loaded
	});
}


function show_post_rating_modal (course_id, course_name)
{
	// fill in modal dialog with HTML markup
	var data = {
		course_id: course_id,
		course_name: course_name
	};
	$('#modal-post-rating').html($.nano($('#tpl-modal-post-rating').html(), data));
	
	// setup interaction
	$('#modal-post-rating .btn-success').click(function () { post_rating(course_id); });
	$('#modal-post-rating form').submit(function () { /*post_rating(course_id);*/ return false; });
	
	// show dialog
	$('#modal-post-rating').modal({
		backdrop: 'static',
		'keyboard': false
	});
}


function post_rating (course_id)
{
	var dlg = $('#modal-post-rating');
	
	// set loading state
	$('.btn-success', dlg).button('loading');
	
	var data = {
		course_id: course_id,
		stars: $('#form-stars', dlg).val(),
		remark: $('#form-remark', dlg).val(),
		student_email: $('#form-email', dlg).val()
	};
	
	$.post('/api/post-rating', data, function (response, status) {
		console.log(status);
		$(dlg).on('hidden', function () { setTimeout(250, function () { location.reload(); }); });
		$(dlg).modal('hide');
	});
	
}



$(document).ready(function () {
	
	$('.course').each(function () {
		
		var course_div = $(this);
		
		// retrieve course data in markup
		var course_id = course_div.attr('data-course-id');
		var course_name = course_div.attr('data-course-name');
		
		// initialize status attributes
		course_div.attr('data-course-opened', 0);
		course_div.attr('data-course-ratings-loaded', 0);
		
		// setup interaction
		$('.course-name', course_div).click(function () { toggle_course(course_div); return false; });
		$('.btn-post-rating', course_div).click(function () {
			show_post_rating_modal(course_id, course_name);
			return false;
		});
	});
	
});
