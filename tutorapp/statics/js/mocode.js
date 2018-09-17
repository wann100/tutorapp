//Code to move the footer up if the mouse is over it
var mousein;
var bottom;
var bottomax;
var bottomstart;
var anim;
bottomstart = -180
mousein = false
bottom = bottomstart
bottomax = 0;
anim = 0;
//$(".footer").mouseenter(function(){menter()});
//$(".footer").mouseleave(function(){mleave()});
function menter(){
	mousein = true
}
function mleave(){
	mousein = false
}

function ftoggle(){
	mousein = !mousein
	anim = 1
	animate()
}

function togglecomments(mydiv,divid){
	var isvisible = $(divid).css('display')
	if(isvisible == 'none'){
		$(divid).css('display','block')
		$(mydiv).attr('src','statics/images/forumuarrow.png')
	}
	if(isvisible == 'block'){
		$(divid).css('display','none')
		$(mydiv).attr('src','statics/images/forumdarrow.png')
	}
}

window.requestAnimFrame = (function(callback) {
return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
function(callback) {
  window.setTimeout(callback, 1000 / 50);
};
})();

function stepevent(){
	if(mousein == true){
		if(bottom < bottomax){
			bottom += 5
			$(".footer").css('bottom',bottom)
			if($("#farrow").attr('src') != 'statics/images/uarrow.png')$('#farrow').attr('src','statics/images/uarrow.png')
		}
		if(bottom >= bottomax){
			if($("#farrow").attr('src') != 'statics/images/darrow.png')$('#farrow').attr('src','statics/images/darrow.png')
			anim = 0
		}
	}
	if(mousein == false){
		if(bottom > bottomstart){
			bottom -= 5
			$(".footer").css('bottom',bottom)
			if($("#farrow").attr('src') != 'statics/images/darrow.png')$('#farrow').attr('src','statics/images/darrow.png')
		}
		if(bottom <= bottomstart){
			if($("#farrow").attr('src') != 'statics/images/uarrow.png')$('#farrow').attr('src','statics/images/uarrow.png')
			anim = 0
		}
	}
}

function animate(){
	stepevent();
	if(anim == 1){
		requestAnimFrame(function() {
		  animate();
		});
	}
}

if(document.title == "Calendar"){
	$("#mycalendertext").attr('class','navclicked')
}
if(document.title == "My Forums"){
	$("#myforumstext").attr('class','navclicked')
}
if(document.title == "My Profile"){
	$("#myprofiletext").attr('class','navclicked')
}
if(document.title == "My Tutors"){
	$("#mytutorstext").attr('class','navclicked')
}

/*------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------*/


(function($) {

         // DOM Ready
        $(function() {

            // Binding a click event
            // From jQuery v.1.7.0 use .on() instead of .bind()
			$('#loginbutton').on('click', function(e) {
				e.preventDefault();
				$('#loginbox').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('.requestbutton').on('click', function(e) {
				e.preventDefault();
				$('#tutorrequestform').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('.cancelbutton').on('click', function(e) {
				e.preventDefault();
				$('#cancelapptbutton').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#add-course').on('click', function(e) {
				e.preventDefault();
				$('#addcourse').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#add-avail').on('click', function(e) {
				e.preventDefault();
				$('#addavailability').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			
			$('.del-class').on('click', function(e) {
				e.preventDefault();
				$('#deleteclass').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('.del-avail').on('click', function(e) {
				e.preventDefault();
				$('#deleteavail').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			
			$('#faqbutton').on('click', function(e) {
				e.preventDefault();
				$('#faqbox').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#informationbutton').on('click', function(e) {
				e.preventDefault();
				$('#vacationinfo').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#informationbuttontwo').on('click', function(e) {
				e.preventDefault();
				$('#vacationinfotwo').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('.contactbutton').on('click', function(e) {
				e.preventDefault();
				$('#contactform').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#functionalitybutton').on('click', function(e) {
				e.preventDefault();
				$('#howitworksbox').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('#areyousurebutton').on('click', function(e) {
				e.preventDefault();
				$('#areyousure').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			$('.avatar').on('click', function(e) {
				e.preventDefault();
				$('#changePhoto').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			
			$('#studentgroupselect').on('click', function(e) {
				e.preventDefault();
				$('#studentpopup').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});
			
			$('.sponpay').on('click', function(e) {
				e.preventDefault();
				$('#sponpop').bPopup({
					modalClose: true
					, fadeSpeed: 'slow'
					, followSpeed: 1500
					, opacity: 0.6
					, modalColor: 'black'
					, zIndex: 20000000
					, transition: 'slideDown'
					, speed: 450
				});
			});

        });

    })(jQuery);