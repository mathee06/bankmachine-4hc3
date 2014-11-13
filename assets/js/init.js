var in_motion = false;
var showing_countdown = false;
var ytPlayer = null;
var contact_form_open = false;
var prevWidth = 0;
var firstLoad = false;
var nbOfTicks = 0;
var videoDefined = false;
	
$(document).ready(function() {
                
	_startLoading();

	// fade in backgrounds, countdown
	$('#bg-image').animate({opacity: 1}, 1000);
		
	// init subscribe form
	/*$(".newsletter form").submit(function (event) {
		event.preventDefault();
		var postData = $(this).serialize();
		var status = $(".newsletter p");
		status.removeClass('shake');
		$.ajax({
			type: "POST",
			url: "scripts/subscription.php",
			data: postData,
			success: function(data) {

				if (data == "success")
					status.html("Thanks for your interest! We will let you know.").slideDown();
				
				else if (data == "subscribed")
					status.toggleClass('shake').html("This email is already subscribed.").slideDown();
				 
				else if (data == "invalid")
					status.toggleClass('shake').html("This email is invalid.").slideDown();
				
				else
					status.toggleClass('shake').html("Oups, something went wrong!").slideDown();	
				
			},
			error: function () {
				status.toggleClass('shake').html("Oups, something went wrong!").slideDown();
			}
		});
	});*/
			
	// init scroll
	if( _isMobile() ) {
		
		_initMobile();

	}else if( _isIpad() ) {

		_initIpad();	

	}else{
		
		_initDesktop();
	}	
	
	_stopLoading();

	$(window).bind('orientationchange resize', function(event){
		_resize();
	});
	
	_resize();

});
      
function _isMobile() {

	return (( /Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent) ) || ($(window).width() <= 568));
}

function _isIpad() {

	return ( /iPad/i.test(navigator.userAgent));
}


function _isDesktop() {

	return (!_isIpad() && !_isMobile());
}

function _isIE() {

	if(typeof($.browser.msie) != "undefined")
		return $.browser.msie;

	return false;
}

function _isIE8Less() {
	return _isIE() && (parseInt($.browser.version) <= 8)
}
function _isIE9Less() {
	return _isIE() && (parseInt($.browser.version) <= 9)
}

function _resize() {

	var winWidth = $(window).width();
	var winHeight = $(window).height();
	var headerHeight = $('div#header').height();
	var contentHeight = winHeight-headerHeight;
	var countdownHeight = $('#countdown-widget').height();

	if(!_isIpad()) {
		var prevWidth = $.cookie('prevWidth');
		if( (winWidth <= 568 && prevWidth > 568) || (winWidth > 568 && prevWidth <= 568)) {
			$.cookie('prevWidth', winWidth);
			prevWidth = $.cookie('prevWidth');
			if(prevWidth)
				location.reload(true);
		}
	}	

	var countdownPaddingTop = (contentHeight / 2) - (countdownHeight / 2) - headerHeight - 30;
	
	var realCountdownWidth = 0;
	$('#countdown-widget .countdown_section').each(function() {
		realCountdownWidth = realCountdownWidth + $(this).width();
	});
	var countdownLeft = ((winWidth - realCountdownWidth) / 2);
	
	if(!_isMobile()) {
		$('#content, div.section.countdown, #widgets').height(contentHeight);
		$('#countdown-widget').css({'left':countdownLeft, 'padding-top':countdownPaddingTop});
		if(contact_form_open) {
			$('#widgets').css('overflow-y', 'hidden');
			$('#contact_form').css({height:contentHeight});
		}else{
			$('#widgets').css('overflow-y', 'hidden');
		}	
	}else{

		$('#countdown-widget').css({'left':countdownLeft});
	}
	
	$("#widgets").getNiceScroll().resize();
	
	if(!showing_countdown)
		_scrollDown();
}

function _initMobile() {
	$("#content").removeAttr('style');

}

function _initIpad() {
	$("#content").removeAttr('style');
	/*$("div.section.countdown").unbind("touchstart");
	
	$("div.section.countdown").bind("touchstart", function() {
		_scrollDown();
	});*/
	
}

function _initDesktop() {
	$("#content").removeAttr('style');
}

function _scrollDown() {

	$('#bg-overlay').stop().animate({'top':0}, 800);

	$('.scrolldown').stop().animate({opacity:0}, 400);
	
	var winHeight = $(window).height();
	$('#content').stop().animate({scrollTop: winHeight}, 800,function(){
		in_motion = false;	
		showing_countdown = false;
		$('#widgets').addClass('opened');		
		$('#content').removeClass('cursor');
	});
	
	if(_isIE8Less()) {
		$('#widgets div.section').fadeIn(1000);
	}else{
		$('#widgets div.section').stop().animate({'opacity':1}, 1800);
	}

	/*$('#countdown-widget').stop().animate({'margin-top':'100px', opacity:0}, 800);*/

}

function _scrollUp() {

	if(contact_form_open)
		$("#contact_form .close").click();
	
	$('#widgets').removeClass('opened');
	$('#bg-overlay').stop().animate({'top':'100%'}, 800);
	if(_isIE8Less()) {
		$('#widgets div.section').fadeOut(1000);
	}else{
		$('#widgets div.section').stop().animate({'opacity':0}, 800);
	}
	$('.scrolldown').stop().animate({opacity:0.8}, 400);
		
	$('#content').stop().animate({scrollTop: 0}, 800,function(){
		in_motion = false;
		showing_countdown = true;	
		$('#widgets').removeClass('opened');
		$('#content').addClass('cursor');
	});
	
	$('#countdown-widget').stop().animate({'margin-top':'0', opacity:0.8}, 800);	
}

function _startLoading() {

	$("#bg-loading").show().animate({opacity:1}, 500);
}

function _stopLoading() {

	timeout = 500;
	if(videoDefined && !firstLoad) {
		timeout = 4000;
		firstLoad = true;
	}
	$(window).load(function() {
		$("#bg-loading").delay(timeout).animate({opacity:0}, 500, function() {
		
			$(this).hide();
		});
	});	
	
}
function _tubularLoaded() {
	return ($('body').find('#tubular-container').length > 0);
}