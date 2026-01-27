var devImage;
var loadingInterval;
var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
var isiPhone = (ua.match(/iphone/i) !== null && !isAndroid && window.innerWidth<737);
var isMiniAndroid = isAndroid && (ua.indexOf("mobile") != -1);

var pix = (window.hasOwnProperty("devicePixelRatio")) ? window.devicePixelRatio: 1;

//FIX: task #1783
var isAnimate = false;

$(document).ready(function () {
    var url = (pix > 2) ? 'img/MouseInfo_LeftPointer@3x.png': 'img/prevDevice.png';
    $("#prevDeviceCell").find(".prevDevice").setAttribute("src", url);

    url = (pix > 2) ? 'img/MouseInfo_RightPointer@3x.png': 'img/nextDevice.png';
    $("#nextDeviceCell").find(".nextDevice").setAttribute("src", url);
});

var renderInit = function () {
    if (isAndroid) {
        $(".resizableText").css("font-size","75%")
    }
    setupSVG();
    onSwipe();
};

var onSwipe = function(){
    //FIX: task #1786
    /*$('#nextDeviceCell').on('touchend', function (event) {
        console.log("touch next");
        stepDevice(1);
    });
    $('#prevDeviceCell').on('touchend', function (event) {
        console.log("touch previous");
        stepDevice(-1);
    });*/

    //FIX: task #1786
    $('#nextDeviceCell').on('touchend', function (event) {
        console.log("touchend next");
        animate(true);
    });
    $('#prevDeviceCell').on('touchend', function (event) {
        console.log("touchend previous");
        animate(false);
    });

    /*if (!isAndroid) {
        $('#deviceInfoTable').on('swiperight', function (event) {
            if (connectedDevices > 1) {
                console.log("swipe previous");
                animateSwipe(true);
            }
        });

        $('#deviceInfoTable').on('swipeleft', function (event) {
            if (connectedDevices > 1) {
                console.log("swipe next");
                animateSwipe(false);
            }
        });
    }*/
};

var offSwipe = function(){
    //FIX: task #1786
    $('#nextDeviceCell').off('touchend');
    $('#prevDeviceCell').off('touchend');

    /*$('#deviceInfoTable').off('swiperight');
    $('#deviceInfoTable').off('swipeleft');*/
};

renderDeviceList = function () {

		if (tagList.length <= 1)
		{
			$(".nextDevice").css('visibility', 'hidden');
			$(".prevDevice").css('visibility', 'hidden');
		}
		else
		{
			$(".nextDevice").css('visibility', "visible");
			$(".prevDevice").css('visibility', "visible");
		}

        var devName = truncate(tagList[getDevIndex()].device, 20);
		$(".deviceName").text(devName);
		localStorage.activeDevice = tagList[getDevIndex()].device;

		loadingInterval = setTimeout(function () { loadImageTimeout($(".devicePic"), tagList[getDevIndex()].image + ".png"); }, 200);
		loadDeviceImage(tagList[getDevIndex()].image);
};

function loadImageTimeout(where, imageURL) {
	var bgImg = new Image();
	bgImg.onload = function () {
		where.css("background-image", "url('" + imageURL + "')");
	};
	bgImg.src = imageURL;
}

renderProfile = function () {
	console.log("render Profile");
    var jcurValue = findDevice(tagValues, localStorage.activeDevice);
    if(jcurValue)
    {
        showDeviceMode(jcurValue);
        loadDeviceImage(tagList[getDevIndex()].image);
        var names = jcurValue.assignments;
        //change profile icon
        if (jcurValue.wireless) {
            if (!jcurValue.isTurnedOn) {
                $(".activeProfile").css("visibility", "hidden");
                return;
            }
        }

        if (jcurValue.hardwareMode != "1") {
            $(".activeProfile").html("<img class='activeProfileCellContent profileIcon' width='50px' height='50px' src='" + jcurValue.profileName + "'/><div id='profileNameText' class='activeProfileCellContent'>" + jcurValue.profileName + jcurValue.mMode + "</div>");
            $(".activeProfile").css("visibility", "visible");
        }
        else {
            $(".activeProfile").css("visibility", "hidden");
        }
    }
};

loadDeviceImage = function (devName) {
    devImage = new Image();
    devImage.onload = renderSVG;
    devImage.src = devName + ".png";

};


renderSVG = function(){

    resetSVG(devImage);
    var curList = findDevice(tagList, localStorage.activeDevice);
    var lines = curList.lines;
    var ll = curList.labels;
    var curValue =findDevice(tagValues, localStorage.activeDevice);
    var lv = curValue.assignments;

    if(!curValue.isTurnedOn || curValue.disabled){ return; }

    if(lines){
    //make lines
        for(var i=0; i < lines.length; i++){
            var line = lines[i];
            //if box is empty, don't draw the corresponding line
            if(findTag(lv, line.ID) !== ""){
                makeLine(line.startX,line.startY,line.endX,line.endY);
            }
        }
    }
    if(ll){
    //fill lines
        for(var i=0; i < ll.length; i++ ){
            var tag = ll[i];
            makeTextBox(findTag(lv,tag.ID), tag.x, tag.y, tag.widthMin, 22 , tag.widthMax);
        }
    }



    $("#gView").off("tap");
    $("#gView").on("tap", function (e) {
        if (e.handled !== true) {
            var nest = document.getElementById("svgView");
            var w = $(nest).attr("data-basewidth");
            var h = $(nest).attr("data-baseheight");

            var padding;
            if (zooming < 2)
            {
                zooming += 0.5;
                padding = zooming * 10;
            }
            else
            {
                zooming = 1;
                padding = 5;
            }

            var numX = (isNaN($("#gView").x)) ? 0 : $("#gView").x;
            var numY = (isNaN($("#gView").y)) ? 0 : $("#gView").y;

            $(nest).css("width", $("#svgImage").attr("width"));
            $(nest).css("height", $("#svgImage").attr("height"));
            $(nest).css("-webkit-transform", "scale("+zooming+")");
            $(nest).css("padding", padding+"em");
            e.handled = true;
        }
    });
};

var showDeviceMode = function(jcurValue) {
    var url;

    var hardwareMode = (jcurValue.hardwareMode == "1") ? ACBridge.tr("onBoardMode") : ACBridge.tr("hostMode");
        $(".deviceMode").text(hardwareMode);
        $(".deviceMode").css("visibility", "visible");
        if (jcurValue.disabled) {

            url = 'img/deviceNotSupportedIcon.png';

            $('#notSupportedMessageText').html("<img src ='"+url+"'/><p>"+ACBridge.tr('deviceNotSupported')+"</p>");
            $("#notSupportedMessage").css("display", "table");
            console.log("device disabled");
            return;
        }
        else {
            $("#notSupportedMessage").css("display", "none");
        }
        if (jcurValue.wireless) {
            if (!jcurValue.isTurnedOn) {

                url = 'img/deviceAsleepIcon.png';

                $('#notSupportedMessageText').html("<img src ='"+url+"'/><p>" + ACBridge.tr('deviceAsleep') + "</p>");
                $(".activeProfile").css("visibility", "hidden");
                $(".deviceMode").css("visibility", "hidden");
                $("#notSupportedMessage").css("display", "table");
                $("#scrollableZone").hide();
                $(".batteryStatus").css("visibility", "hidden");
                console.log("device is not turned on");
                return;
            }
            else {
                $(".batteryStatus").css("visibility", "visible");
                var batteryPercentageString = "";
                var batteryInt = Math.round(Math.round(jcurValue.batteryPercentage / 10) / 2) * 20;
                if(batteryInt > 100 || batteryInt < 0){ batteryInt=0;}
                $(".batteryStatus").html("<img src='img/1x1.gif' class='battery" + batteryInt + "' id='batteryPic'/>");
                //$(".batteryStatus").html("<img id='batteryPic' src='img/battery" + batteryInt + ".png' height=70%>");
                $("#notSupportedMessage").css("display", "none");
            }
        }
        else {
            $(".batteryStatus").css("visibility", "hidden");
        }
};

var endPos = 0;
var startPos = 0;
var swipeTime = 400;
var orig;
var curInfo;

var duplicate = function(direction){
    offSwipe();
    orig = $("#deviceInfoTable");
    orig.toggleClass("sliding");
    orig.css("width",orig.width());
    $("#deviceInfoWrapper").css("width","206%");
    curInfo = orig.clone(false);
    //curInfo.attr("id","Duplicate");
    //curInfo.find("*").removeAttr("id");
    curInfo.find(".devicePic, .deviceName, .deviceMode, .activeProfile, .batteryStatus").removeAttr("class");
    curInfo.addClass("sliding");
    if(direction){
        startPos = "-47%";
        endPos = "3%";
        $("#deviceInfoWrapper").append(curInfo);
    }
    else{
        startPos = "3%";
        endPos = "-47%";
        $("#deviceInfoWrapper").prepend(curInfo);
    }

    stepDevice(direction?1:-1);

        curInfo.css("left",startPos);
        orig.css("left", startPos);

};
var animate = function(direction){

    if (isAnimate)
        return;
    isAnimate = true;

    //FIX: task #1786
    offSwipe();
    stepDevice(direction?1:-1);
    onSwipe();

    setTimeout(function() {
        isAnimate = false;
    }, 100);
            /*orig.css("opacity",0);
        orig.animate(
            {"left": endPos+"%", opacity:1},
            swipeTime
        );
        curInfo.animate(
            {"left" : endPos + "%", opacity:0},
            swipeTime,
             function(){
                orig.toggleClass("sliding");
                orig.css("width","");
                $("#deviceInfoWrapper").css("width", "");
                curInfo.remove();
                onSwipe();
            }
        );*/
};
var animateSwipe = function(direction){
    duplicate(direction);
    animate(direction);
};
