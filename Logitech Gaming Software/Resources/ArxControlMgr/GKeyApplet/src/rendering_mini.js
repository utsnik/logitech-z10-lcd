var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
var isiPhone = (ua.match(/iphone/i) !== null && !isAndroid && window.innerWidth<737);
var isMiniAndroid = isAndroid && (ua.indexOf("mobile") != -1);

var pix = (window.hasOwnProperty("devicePixelRatio")) ? window.devicePixelRatio: 1;

$(document).ready(function () {
	var url = (pix > 2) ? 'img/LoadingSpinner@3x.gif': 'img/loading.gif';
	$("#deviceImage").setAttribute("src", url);
});

var stepDevice = function (dir) {
	var di = getDevIndex() + dir;
	if(di < 0){ di = tagList.length-1;}
	di = di% tagList.length;
	setDevIndex(di);
	renderProfile();
};

var animateDevice = function(dir){
	if (isAnimate)
		return;

	selectStop();
	var orig = $("#deviceImage");
	var copy = orig.clone();
	stepDevice(dir);
	$("#deviceSelector").append(copy);
	var origPos = {end: copy.width()/2, start: dir * 200};
	var copyPos = {end: -dir*200, start: -orig.width()/2};
	var duration = 500;
	copy.attr("id", "devImgclone");
	orig.css("left", origPos.start);
	copy.css("left", copyPos.start);
	orig.css("opacity", 0);
	orig.animate({left:origPos.end, opacity:1}, duration);
	copy.animate({left:copyPos.end, opacity:0}, duration,
		function(){
			copy.remove();
			orig.css("left","");
			selectListen();
	});
};
//FIX: task #1783
var isAnimate = false;
var selectListen = function(){
	isAnimate = false;
	$("#nextDev").on("click", function(){
		animateDevice(1);
	});
	$("#prevDev").on("click", function(){
		animateDevice(-1);
	});
	if (!isAndroid) {
	    $("#deviceSelector").on("swipeleft", function () {
	        animateDevice(1);
	    });

	    $("#deviceSelector").on("swiperight", function () {
	        animateDevice(-1);
	    });
	}
};
var selectStop = function(){
	isAnimate = true;
	$("#nextDev, #prevDev").off("click");
	$("#deviceSelector").off("swipeleft swiperight");
};
renderInit = function()
{	selectListen();
};

findVal = function (key, list) {
    if (!list)
        return "";
	for(var i=0; i < list.length; i++){
		if(key == list[i].contextID){
			return list[i].macroName;
		}
	}
	return "";
};

function profileOrOnboard(jcurValue, di) {
	  var hardwareMode = (jcurValue.hardwareMode == "1") ? ACBridge.tr("onBoardMode") : jcurValue.profileName + jcurValue.mMode;
      return hardwareMode;
}

renderProfile = function(){
//	refreshDevImage();
	var jcurValue = findDevice( tagValues, tagList[getDevIndex()].device);
	var jcurKey = tagList[getDevIndex()];
	var url;

	//clear out all children.
	$("#GKeyAssignments").empty();

	if(jcurValue)
	{
		console.log('device asleep' + !jcurValue.isTurnedOn);
		if (jcurValue.disabled) {

			url = 'img/deviceNotSupportedIcon.png';

			$('#notSupportedMessageTextPhone').html("<img src ='"+url+"'/><p>" + ACBridge.tr('deviceNotSupported') + "</p>");
			$("#notSupportedMessagePhone").css("display", "table");
						console.log("returning, device disabled");
			return;
		}
		else {
			$("#notSupportedMessagePhone").css("display", "none");
		}
		if (!jcurValue.isTurnedOn) {

			url = 'img/deviceAsleepIcon.png';

			$('#notSupportedMessageTextPhone').html("<img src ='"+url+"'/><p>" + ACBridge.tr('deviceAsleep') + "</p>");
			$("#notSupportedMessagePhone").css("display", "table");
			console.log("returning, device not on");
			return;
		}
		else {
			$("#notSupportedMessagePhone").css("display", "none");
		}
		var names = jcurKey.labels;
		//sort on found number
		names.sort( function(a,b){
			var findNum = /\d+/;
			var numa = findNum.exec(a.ID);
			var numb = findNum.exec(b.ID);
			return parseInt (numa) - parseInt (numb);
		});

		for (var i = 0; i < names.length ; i++) {
			var asn = names[i];
			if(asn){
				var val = findVal(asn.ID, jcurValue.assignments);
				var idName = asn.ID.replace("Button", "G");
				var entry = "<tr><td ><div class='macroBtn'>"+idName+"</div></td><td>"+val+"</td></tr>";
				$("#GKeyAssignments").append(entry);
			}
		}
	}
	else{
		console.log("did not enter jcurValue");
	}


    var di = getDevIndex();
	$("#profileName").text(profileOrOnboard(jcurValue, di));
	$("#deviceImage").attr('src', tagList[di].image + ".png");
};

renderDeviceList = function() {
	var di = getDevIndex();
	var jcurValue = findDevice( tagValues, tagList[di].device);

	$("#profileName").text(profileOrOnboard(jcurValue, di));
	$("#deviceImage").attr('src', tagList[di].image + ".png");
};
