var deviceVisualizedIndex = 0;
var connectedDevices = 0;
var dpiXSlider;
var dpiYSlider;
var dpiValuesArray_X = [];
var dpiValuesArray_Y = [];
var minDpi, maxDpi, dpiStep;
var initialization = true;
var xYsync = true;
var ySliderPresent = false;
var deviceName = "";
var deviceModel = "";
var mode = "";
var hardware = "";
var activeProfile = "";
var activeProfileID = "";
var currentDpiIndex = 0;
var shiftDpiIndex = 0;
var defaultDpiIndex = 0;
var global = "0";
var isDeviceWireless = "";
var isCharging = "";
var isTurnedOn = "";
var batteryPercentage = "";
var loadingInterval;
var loadingIntervalProfile;
var deviceSupported = "";
var nextZlevel = 1;
var isRenderingOnIPhone = ($(window).width() <= 640 || window.innerHeight < 550);
var currentDpiIndexHandle = 0;
var profileChanged = true;
var sendDpiDataTimeout;
var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
var isiPhone = (ua.match(/iphone/i) !== null && !isAndroid && window.innerWidth<737);
var isMiniAndroid = isAndroid && (ua.indexOf("mobile") != -1);

var pix = (window.hasOwnProperty("devicePixelRatio")) ? window.devicePixelRatio: 1;
var adjustBoxSizes = false;

//FIX: task #1783
var isAnimate = false;

function doSliderBoxAdjustment()
{
	if (adjustBoxSizes == true)
	{
		$("#blackBoxSliderX").css('height','50%');
		$("#dpiButtonControlX").css('height','45%');
	}
}
$(document).ready(function () {
 if (isiPhone || isMiniAndroid || window.innerWidth < 700 || window.innerHeight < 550) {
        $("#layout").attr({ href: "styleSheetPhone.css" });
        //For some reason this fixes some layout issues on Android 4.4
        $("#deviceInfoPhone").hide();
        $("#deviceInfoPhone").show();
    }
    else {
        $("#layout").attr({ href: "styleSheet.css" });
		if (isAndroid)
		{
			adjustBoxSizes=true;
			doSliderBoxAdjustment();
		}
    }

    //FIX: task #1888
    if (isAndroid) {
        $("#initialProperty").hide();
       // $("#deviceInfoWrapper").hide();
    }
	$("#notSupportedMessage").hide();

    if (isDeviceWireless != "yes") {
        $(".batteryStatus").css('display', 'none');
        $(".batteryStatusMargin").css('display', 'none');
    }

    $(window).bind("orientationchange", function (event) {
        repositionSliderUI();
    });


    //var url = (pix > 2) ? 'img/MouseInfo_LeftPointer@3x.png': 'img/prevDevice.png';
    //$("#prevDeviceCell").find(".prevDevice").setAttribute("src", url);

    //url = (pix > 2) ? 'img/MouseInfo_RightPointer@3x.png': 'img/nextDevice.png';
    //$("#nextDeviceCell").find(".nextDevice").setAttribute("src", url);

    //url = (pix > 2) ? 'url("img/MouseInfo_AxisLabelX@3x.png")': 'url("img/xSliderBack.png")';
    //$("#blackBoxSliderX").css('background-image',url);

    ACBridge.log(isiPhone + ' ' + isMiniAndroid + ' ' + window.innerWidth);

});

function cached(url){
    var test = document.createElement("img");
    test.src = url;
    return test.complete || test.width+test.height > 0;
}

String.prototype.trunc = String.prototype.trunc ||
      function (n) {
          return this.length > n ? this.substr(0, n - 1) + '&hellip;' : this.substr(0, this.length);
      };


function sortNumber(a, b) {
    return a - b;
}

function sortHandles(a, b) {
    var $aa = $(a);
    var $bb = $(b);
    return parseInt($aa.find('.value-label').html()) - parseInt($bb.find('.value-label').html());
}

function hasClass(element, cls) {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
}

var renderControlArrows = function(axis, valToSet){
    var url;

    if (valToSet == maxDpi) { //can't go any higher than this
        url = (pix > 2) ? 'url("img/dpiControlUpDisabled.png")': 'url("img/dpiControlUpDisabled.png")';
        $(".dpiControlUp").css("background-image", url);
    }
    else{
        url = (pix > 2) ? 'url("img/MouseInfo_StepperIncrease@3x.png")': 'url("img/dpiControlUp.png")';
        $(".dpiControlUp").css("background-image", url);
    }
    if (valToSet == minDpi ) { //can go at least one step down
        url = (pix > 2) ? 'url("img/dpiControlDownDisabled.png")': 'url("img/dpiControlDownDisabled.png")';
        $(".dpiControlDown").css("background-image", url);
    }
    else{
        url = (pix > 2) ? 'url("img/MouseInfo_StepperDecrease@3x.png")': 'url("img/dpiControlDown.png")';
        $(".dpiControlDown").css("background-image", url);
    }
};

var sendDpiData = function (lastUsedSlider) {

    var values_X = $("#dpiSliderX").slider("values");
    var values_Y;
    var sync = (xYsync == "synced") ? "1" : "0";
    if (sync == "1")
        values_Y = values_X;
    else
        values_Y = $("#dpiSliderY").slider("values");

    var hardwareFlag = (hardware == "1") ? "1" : "0";
    var labels = $("#dpiSlider" + lastUsedSlider + " > .ui-slider-handle");
    sortedHandles = labels.sort(sortHandles);
    for (var i = 0; i < sortedHandles.length; i++) {
        if (hasClass(sortedHandles[i], "currentDpiIndex")) {
            currentDpiIndex = i;
        }
        if (hasClass(sortedHandles[i], "shiftDpiIndex")) {
            shiftDpiIndex = i;
        }
        if (hasClass(sortedHandles[i], "defaultDpiIndex")) {
            defaultDpiIndex = i;
        }
    }
    var clickEventString = "sync:" + sync + "|dpiSliderX:" + values_X.sort(sortNumber).join(",") + "|dpiSliderY:" + values_Y.sort(sortNumber).join(",") + "|currentDpiIndex:" + currentDpiIndex + "|shiftDpiIndex:" + shiftDpiIndex + "|defaultDpiIndex:" + defaultDpiIndex + "|deviceName:" + deviceName + "|deviceModel:" + deviceModel + "|mode:" + mode + "|hardware:" + hardwareFlag + "|global:" + global + "|activeProfile:" + activeProfile + "|activeProfileID:" + activeProfileID;
    ACBridge.click(clickEventString);
    ACBridge.log("currentDpi sent:" + currentDpiIndex);
    //Disable any further user interaction
    $("#waitingForResponseLayer").show();
};

var getNextAvailableDpiValue = function (initialValue, axis, goingUp) { //goingUp = true ->looks for next available val higher, if false looks for a lower value
    var candidateValue = initialValue;
    var valuesArray = [];
    if (axis == "X")
        valuesArray = dpiValuesArray_X;
    else
        valuesArray = dpiValuesArray_Y;
    valuesArray.splice(currentDpiIndex, 1);
    var goingUp = goingUp; //looking for next val higher or lower
    while (($.inArray(candidateValue, valuesArray) != -1)) {
        if (goingUp) {
            if ((candidateValue + dpiStep) > maxDpi) {
                goingUp = false;
                continue;
            }
            candidateValue+=dpiStep;
        }
        else {
            if ((candidateValue - dpiStep) < minDpi) {
                //If it enters here there is no available value, let's set it to default
                candidateValue = valuesArray[defaultDpiIndex];
            }
            candidateValue-=dpiStep;
        }
    }
    return candidateValue;
}

resizeBatteryDisplay = function () {
    var batteryShown = $(".batteryStatus").css("visibility") != "hidden";
    var newwidth = batteryShown ? "" : "93.5%" ;
    $("#deviceInfoTextPhone").css("width", newwidth);
};


onPropertyUpdate = function () {
    isAnimate = false;

    $("#waitingForResponseLayer").hide();

    var startingValue = 0;
	var currDevice = document.getElementById("currentlyDisplayedDevice");
	if (currDevice != null)
	{
		var value = currDevice.getAttribute('value');
		deviceVisualizedIndex = parseInt(value);
	}
//    deviceVisualizedIndex = parseInt(document.getElementById("currentlyDisplayedDevice").getAttribute('value'));
    currDevice = document.getElementById("connectedDevices");
	if (currDevice != null)
	{
		var value = currDevice.getAttribute('value');
		connectedDevices = parseInt(value);
	}
	//connectedDevices = parseInt(document.getElementById("connectedDevices").getAttribute('value'));
    if (connectedDevices <= 1) {
        $(".nextDevice").css('display', 'none');
        $(".prevDevice").css('display', 'none');
    }
    else {
        $(".nextDevice").css('display', '');
        $(".prevDevice").css('display', '');
    }
    deviceSupported = document.getElementById("deviceSupported").getAttribute('value');
    deviceName = document.getElementById("deviceName").getAttribute('value');
    if (document.getElementById("deviceModel").getAttribute('value') != deviceModel) //got new device model
    {
        deviceModel = document.getElementById("deviceModel").getAttribute('value');
        var modelImg = deviceModel + ".png";

        if($(".devicePic").hasClass('loading')) {
            $(".devicePic").removeClass('loading');
        }

        if(!cached(modelImg)){
           loadingInterval = setInterval(function () { loadImageTimeout($(".devicePic"), modelImg); }, 200);
        }
        else{
            $(".devicePic").css("background-image", "url('" + modelImg + "')");
        }
    }
    deviceModel = document.getElementById("deviceModel").getAttribute('value');
    mode = document.getElementById("mode").getAttribute('value');
    hardware = document.getElementById("hardware").getAttribute('value');
    global = document.getElementById("global").getAttribute('value');
    if (hardware == "1")
        activeProfile = ACBridge.tr("noProfile");
    else {
        if (global == "1")
            activeProfile = ACBridge.tr("globalDpi");
        else
            activeProfile = document.getElementById("activeProfile").getAttribute('value');
    }
    if (document.getElementById("activeProfileID").getAttribute('value') != activeProfileID) {
        profileChanged = true;
    }
    else {
        profileChanged = false;
    }
    activeProfileID = document.getElementById("activeProfileID").getAttribute('value');

    isDeviceWireless = document.getElementById("isDeviceWireless").getAttribute('value');
    isCharging = document.getElementById("isCharging").getAttribute('value');
    isTurnedOn = document.getElementById("isTurnedOn").getAttribute('value');
    batteryPercentage = document.getElementById("batteryPercentage").getAttribute('value');
    var hardwareMode = (hardware == "1") ? ACBridge.tr("onBoardMode") : ACBridge.tr("hostMode");
    $(".deviceMode").text(hardwareMode);
    $(".deviceMode").css('visibility', 'visible');
    $(".deviceName").text(deviceName);

    if (isDeviceWireless == "yes") {
        if (isTurnedOn == "no") {

            var url = 'img/deviceAsleepIcon.png';

            $('#notSupportedMessageText').html("<img src ='"+url+"'/><p>" + ACBridge.tr("deviceAsleep")+"</p>");

            $(".activeProfile").css('visibility', 'hidden');
            activeProfileID = "";
            $(".deviceMode").css('visibility', 'hidden');
            $(".profileIcon").css('visibility', 'hidden');
            $("#notSupportedMessage").css("display", "table");

            /*$("#scrollableZone").hide();*/
            $("#dpiSliderX_wrapper").hide();
            $("#dpiSliderY_wrapper").hide();

            /*$(".batteryStatus").css('visibility', 'hidden');*/
            $(".batteryStatus").css('display', 'none');
            $(".batteryStatusMargin").css('display', 'none');
            /*resizeBatteryDisplay();*/
            return;
        }
        else {
            var batteryPercentageString = "";
            var batteryInt = Math.round(Math.round(batteryPercentage / 10) / 2) * 20;
            if(batteryInt > 100 || batteryInt < 0){ batteryInt=0;}
            $(".batteryStatus").html("<img src='img/1x1.gif' class='battery" + batteryInt + "' id='batteryPic'/>");
            $(".batteryStatus").css('display', 'table-cell');
            $(".batteryStatusMargin").css('display', 'table-cell');
                        /*resizeBatteryDisplay();*/

        }
    }
    else {
        $(".batteryStatus").css('display', 'none');
        $(".batteryStatusMargin").css('display', 'none');
                    /*resizeBatteryDisplay();*/

    }

    if (deviceSupported == "0") {
        $(".activeProfile").css('visibility', 'hidden');
        activeProfileID = "";

        var url = 'img/deviceNotSupportedIcon.png';

        $('#notSupportedMessageText').html("<img src ='"+url+"'/><p>"+ACBridge.tr("deviceNotSupported")+"</p>");
        $("#notSupportedMessage").css("display", "table");

        /*$("#scrollableZone").hide();*/
        $("#dpiSliderX_wrapper").hide();
        $("#dpiSliderY_wrapper").hide();

        return;
    }
    else if (deviceSupported == "1") {

        $("#notSupportedMessage").css("display", "none");

        /*$("#scrollableZone").show();*/
        $("#dpiSliderX_wrapper").show();
        $("#dpiSliderY_wrapper").show();

        if (profileChanged) {
            if (hardware == "0" && global == "0") {
                $(".activeProfile").html("<img class='activeProfileCellContent loading profileIcon' width='50px' height='50px' alt='loading'/><div id='profileNameText' class='activeProfileCellContent'>" + activeProfile.trunc(30) + "</div>");/* src='loading.gif'*/
                $(".activeProfile").css('visibility', 'visible');
                $(".profileIcon").css('visibility', 'hidden');
                loadingIntervalProfile = setInterval(function () { loadProfileIconTimeout($(".profileIcon"), activeProfile + ".png"); }, 200);
            }
            else {
                if (global == "1") {
                    activeProfile = "" + ACBridge.tr("globalDpi");
                    $(".activeProfile").html(activeProfile);
                    $(".activeProfile").css('visibility', 'visible');
                }
                else {
                    $(".activeProfile").html(activeProfile.trunc(30));
                    $(".activeProfile").css('visibility', 'visible');
                }
            }
        }
        currentDpiIndex = parseInt(document.getElementById("currentDpiIndex").getAttribute('value'));
        shiftDpiIndex = parseInt(document.getElementById("shiftDpiIndex").getAttribute('value'));
        defaultDpiIndex = parseInt(document.getElementById("defaultDpiIndex").getAttribute('value'));
        ACBridge.log("currentDpi received:" + currentDpiIndex);
        dpiValuesArray_X = [];
        dpiValuesArray_Y = [];
        var dpiValuesElements_X = document.getElementById("dpiSliderX").getElementsByTagName('a');
        for (var i = 0; i < dpiValuesElements_X.length; i++) {
            dpiValuesArray_X[i] = parseInt(dpiValuesElements_X[i].getAttribute('value'));
        }

        var dpiValuesElements_Y = document.getElementById("dpiSliderY").getElementsByTagName('a');
        for (i = 0; i < dpiValuesElements_Y.length; i++) {
            dpiValuesArray_Y[i] = parseInt(dpiValuesElements_Y[i].getAttribute('value'));
        }

        minDpi = parseInt(document.getElementById("minDpi").getAttribute('value'));
        maxDpi = parseInt(document.getElementById("maxDpi").getAttribute('value'));
        dpiStep = parseInt(document.getElementById("dpiStep").getAttribute('value'));
        xYsync = document.getElementById("xYsync").getAttribute('value');

        renderControlArrows("X", dpiValuesArray_X[currentDpiIndex] );
        renderControlArrows("Y", dpiValuesArray_Y[currentDpiIndex] );

        $("#dpiControlCurrent_X").text(dpiValuesArray_X[currentDpiIndex]);
        $("#dpiControlCurrent_Y").text(dpiValuesArray_Y[currentDpiIndex]);

        $(".ui-slider-handle").find('.value-label').css("color", "#BDBDBD");
        $(".currentDpiIndex").find('.value-label').css("color", "white");

        if (dpiXSlider)
            dpiXSlider.slider("destroy");

        dpiXSlider = $("#dpiSliderX").slider({
            min: minDpi,
            max: maxDpi,
            step: dpiStep,
            values: dpiValuesArray_X,
            start: function (event, ui) {
                startingValue = ui.value;
                if(!$(ui.handle).find('.value-label').hasClass('current'))
                    $(ui.handle).find('.value-label').toggleClass('current');
                $(ui.handle).css("z-index", ++nextZlevel);
                $('#dpiSliderY > .ui-slider-handle').eq($(ui.handle).index()).css("z-index", nextZlevel);
            },
            slide: function (event, ui) {
                currentDpiIndex = $(ui.handle).index();
                $(ui.handle).find('.value-label').text(ui.value);
            },
            change: function (event, ui) {
                if ($(ui.handle).find('.value-label').hasClass('current'))
                    $(ui.handle).find('.value-label').toggleClass('current');
                currentDpiIndexHandle = $(ui.handle).index();
                $(".currentDpiIndex").toggleClass("currentDpiIndex");
                $('#dpiSliderX > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
                $('#dpiSliderY > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
                var changedValue = 0;
                if (ui.value != startingValue)
                    changedValue = getNextAvailableDpiValue(ui.value, "X", true);
                else
                    changedValue = ui.value;
                if(changedValue != ui.value)
                    $("#dpiSliderX").slider("values", currentDpiIndexHandle, changedValue);
                $(ui.handle).find('.value-label').text(changedValue);
                $("#dpiControlCurrent_X").text(changedValue);
                dpiValuesArray_X = $("#dpiSliderX").slider("values");
                $(".ui-slider-handle").find('.value-label').css("color", "#BDBDBD");
                $(".currentDpiIndex").find('.value-label').css("color", "white");
                sendDpiData("X");
                renderControlArrows("X", changedValue);
            }
        });

        if (xYsync != "synced") {
            ySliderPresent = true;
            if (dpiYSlider)
                dpiYSlider.slider("destroy");

            dpiYSlider = $("#dpiSliderY").slider({
                min: minDpi,
                max: maxDpi,
                step: dpiStep,
                values: dpiValuesArray_Y,
                start: function (event, ui) {
                    startingValue = ui.value;
                    if (!$(ui.handle).find('.value-label').hasClass('current'))
                        $(ui.handle).find('.value-label').toggleClass('current');
                    $(ui.handle).css("z-index", ++nextZlevel);
                    $('#dpiSliderX > .ui-slider-handle').eq($(ui.handle).index()).css("z-index", nextZlevel);
                },
                slide: function (event, ui) {
                    currentDpiIndex = $(ui.handle).index();
                    $(ui.handle).find('.value-label').text(ui.value);
                },
                change: function (event, ui) {
                    if ($(ui.handle).find('.value-label').hasClass('current'))
                        $(ui.handle).find('.value-label').toggleClass('current');
                    currentDpiIndexHandle = $(ui.handle).index();
                    $(".currentDpiIndex").toggleClass("currentDpiIndex");
                    $('#dpiSliderX > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
                    $('#dpiSliderY > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
                    var changedValue = 0;
                    if (ui.value != startingValue)
                        changedValue = getNextAvailableDpiValue(ui.value, "y", true);
                    else
                        changedValue = ui.value;
                    if (changedValue != ui.value)
                        $("#dpiSliderY").slider("values", currentDpiIndexHandle, changedValue);
                    $(ui.handle).find('.value-label').text(changedValue);
                    $("#dpiControlCurrent_Y").text(changedValue);
                    dpiValuesArray_Y = $("#dpiSliderY").slider("values");
                    $(".ui-slider-handle").find('.value-label').css("color", "#BDBDBD");
                    $(".currentDpiIndex").find('.value-label').css("color", "white");
                    sendDpiData("Y");
                    renderControlArrows("Y", changedValue);
                }
            });
            $("#blackBoxSliderX").css("background-image", "");
        }
        else {
            ySliderPresent = false;
            $("#blackBoxSliderX").css("background-image", "url('img/xSliderBack.png')");
        }


        repositionSliderUI();

        $(".ui-slider-handle").click(function (event) {
            $(".currentDpiIndex").toggleClass("currentDpiIndex");
            currentDpiIndexHandle = $(this).index();
            $('#dpiSliderX > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
            $('#dpiSliderY > .ui-slider-handle').eq(currentDpiIndexHandle).toggleClass("currentDpiIndex");
            sendDpiData("X");
        });

        $(".ui-slider-handle.defaultDpiIndex").append("<div class='diamondDefault'/>");

        nextZlevel += 2;
        $('#dpiSliderX > .ui-slider-handle').eq(currentDpiIndex).css("z-index", nextZlevel);
        $('#dpiSliderY > .ui-slider-handle').eq(currentDpiIndex).css("z-index", nextZlevel);
    }
    doSliderBoxAdjustment();
};

function repositionSliderUI() {
    if (ySliderPresent) {
        if (isRenderingOnIPhone) {

            if (window.innerWidth > window.innerHeight) {
                //in landscape mode
                $("#dpiSliderX_wrapper").css("top", "38%");
                $("#dpiSliderX_wrapper").css("right", "50%");
                $("#dpiSliderX_wrapper").css("bottom", "25%");
                $("#dpiSliderX_wrapper").css("left", "1%");
                $(".dpiSliderWrapper").css("height", "30%");
            }
            else {
                //in portrait
                $(".dpiSliderWrapper").css("height", "15%");
                $("#dpiSliderX_wrapper").css("top", "0%");
                $("#dpiSliderX_wrapper").css("right", "0%");
                $("#dpiSliderX_wrapper").css("bottom", "0%");
                $("#dpiSliderX_wrapper").css("left", "0%");
            }
        }
    }
    else {
        //there is no Y slider
        $("#dpiSliderY_wrapper").css('display', 'none');
        $("#blackBoxSliderX").css('background-image', 'none');
        if (isRenderingOnIPhone) {
            if (window.innerWidth > window.innerHeight) {
                //in landscape mode
                $("#dpiSliderX_wrapper").css("top", "38%");
                $("#dpiSliderX_wrapper").css("right", "1%");
                $("#dpiSliderX_wrapper").css("bottom", "30%");
                $("#dpiSliderX_wrapper").css("left", "1%");
                $(".dpiSliderWrapper").css("height", "30%");
            }
            else {
                //portrait
                $(".dpiSliderWrapper").css("height", "30%");
                $("#dpiSliderX_wrapper").css("top", "0%");
                $("#dpiSliderX_wrapper").css("right", "0%");
                $("#dpiSliderX_wrapper").css("bottom", "0%");
                $("#dpiSliderX_wrapper").css("left", "0%");
            }

        }
    }
}

function loadImageTimeout(where, imageURL) {

    var bgImg = new Image();
    bgImg.onload = function () {
        where.css("background-image", "url('" + imageURL + "')");
        clearInterval(loadingInterval);
    };
    bgImg.src = imageURL;
}

function loadProfileIconTimeout(where, imageURL) {
    var img = new Image();
    img.onload = function () {
        where.css('visibility', 'visible');
        where.attr('src', imageURL);
        clearInterval(loadingIntervalProfile);
        where.fadeIn();
        where.removeClass("loading");
    };
    img.src = imageURL;
}

function requestDeviceInfo(nextOrPrevious){
    if (isAnimate)
        return;
    isAnimate = true;

    if (!nextOrPrevious) {
        if (deviceVisualizedIndex > 0)
            deviceVisualizedIndex--;
        else
            deviceVisualizedIndex = connectedDevices - 1;
    }
    else {
        if (deviceVisualizedIndex < (connectedDevices - 1))
            deviceVisualizedIndex++;
        else
            deviceVisualizedIndex = 0;
    }

    ACBridge.click("deviceSelect|" + deviceVisualizedIndex);

    if(!$(".devicePic").hasClass('loading')) {
        $(".devicePic").addClass('loading');
    }
    //$(".devicePic").css('background-image', "url('img/loading.gif')");

    activeProfileID = "";
}

var onACBridgeLoad = function(){

    ACBridge.trLoadStrings();
    ACBridge.trAll();
    init();
};

var onSwipe = function(){
    $('.nextDevice').on('tap', function (event) {
        requestDeviceInfo(true);
    });

    $('.prevDevice').on('tap', function (event) {
        requestDeviceInfo(false);
    });

    //FIX: task #1881
    /*if (!isAndroid) {
        $('#deviceInfoTable').on('swiperight', function (event) {
            if (connectedDevices > 1) {
                animateSwipe(true);
            }
        });
        $('#deviceInfoTable').on('swipeleft', function (event) {
            if (connectedDevices > 1) {
                animateSwipe(false);
            }
        });
        $("#deviceSelectorPhone").on("swiperight", function () {
            if (connectedDevices > 1) {
                animateSwipePhone(false);
            }
        });
        $("#deviceSelectorPhone").on("swipeleft", function () {
            if (connectedDevices > 1) {
                animateSwipePhone(true);
            }
        });
    }*/

};
var offSwipe = function(){
    $('#nextDevice').off('tap');
    $('#prevDevice').off('tap');
};

var init = function () {
    onSwipe();
    if (!isRenderingOnIPhone) {
        $(".dpiControlDown_Horizontal").css('display', 'none');
        $(".dpiControlUp_Horizontal").css('display', 'none');

        $("#deviceSelectorPhone").hide();
        $("#deviceInfoPhone").hide();

    } else {
        $(".dpiControlUp").css('display', 'none');
        $(".dpiControlDown").css('display', 'none');
        $("#deviceInfoWrapper").hide();
    }

    var stepSliders = function(axis, step, goingUp){
        currentDpiIndexHandle = $("#dpiSlider"+axis+" > .currentDpiIndex").index();
        var curValue = $("#dpiSlider"+axis).slider("values", currentDpiIndexHandle);
        var valToSet = curValue + step;
        if(valToSet < minDpi || valToSet > maxDpi)
            return;
        valToSet = getNextAvailableDpiValue(valToSet, axis, goingUp);
        $("#dpiSlider"+axis).slider("values", currentDpiIndexHandle, valToSet);
        $("#dpiControlCurrent_"+axis).text(valToSet);
        $("#dpiSlider"+axis).find(".currentDpiIndex").find('.value-label').text(valToSet);
        renderControlArrows(axis, valToSet);
    };

    $('.dpiStepUpX').on('touchend', function () {
        stepSliders("X", dpiStep, true);
    });

    $('.dpiStepDownX').on('touchend', function () {
       stepSliders("X", -1 * dpiStep, false);
    });

    $('.dpiStepUpY').on('touchend', function () {
        stepSliders("Y", dpiStep, true);
    });

    $('.dpiStepDownY').on('touchend', function () {
        stepSliders("Y", -1 * dpiStep, false);
    });



};
