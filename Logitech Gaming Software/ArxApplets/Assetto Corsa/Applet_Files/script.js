var currentFrontDamage = -1.0;
var currentBackDamage = -1.0;
var currentLeftDamage = -1.0;
var currentRightDamage = -1.0;
var currentMaxRpm = 0;
var currentGear = 0;
var currentPage = 1;
var currentStatus = "Unknown";
var swipeInProgress = false;
var dotColor="#990000";
var isIPhone = false;
function replaceAll(find, replace, str) {
    return str.replace(new RegExp(find, 'g'), replace);
}

var animateSwipe = function (pageNum) {
    swipeInProgress = true;
    var swipeTime = 400;
    if (pageNum == 1) {
        if (currentPage != 1) {
            $(".pageDiv").show();
            $("#firstPage").animate(
                { "left": 0 + "%", opacity: 1 },
                swipeTime,
                function() {
                    // Animation complete.
                    if (isIPhone)
                        $("#secondPage").hide();
                    swipeInProgress = false;
                }   
            );
            $("#secondPage").animate(
                { "left": 100 + "%", opacity: 1 },
                swipeTime,
                function() {
                    // Animation complete.
                    swipeInProgress = false;
                }
            );
            currentPage = 1;
            
            $(".pageDot").eq(0).css("background-color", dotColor);
            $(".pageDot").eq(1).css("background-color", "transparent");
        }
        else {//bounce
            $("#firstPage").animate(
                { "left": 3 + "%", opacity: 1 },
                swipeTime/4
            );
            $("#firstPage").animate(
                { "left": 0 + "%", opacity: 1 },
                swipeTime / 4
            );
        }
    }
    else if (pageNum == 2) {
        $(".pageDiv").show();
        if(isIPhone)
            $("#secondPage").show();
        if (currentPage != 2) {
            $("#firstPage").animate(
                { "left": -100 + "%", opacity: 1 },
                swipeTime,
                function () {
                    // Animation complete.
                    swipeInProgress = false;
                }
            );
            $("#secondPage").animate(
                { "left": 0 + "%", opacity: 1 },
                swipeTime,
                function () {
                    // Animation complete.
                    swipeInProgress = false;
                }
            );
            currentPage = 2;
            $(".pageDot").eq(1).css("background-color", dotColor);
            $(".pageDot").eq(0).css("background-color", "transparent");
        }
        else {
            //bounce
            $("#secondPage").animate(
               { "left": -3 + "%", opacity: 1 },
               swipeTime / 4
           );
            $("#secondPage").animate(
                { "left": 0 + "%", opacity: 1 },
                swipeTime / 4
            );
        }
    }
};

update = function () {
    //STATUS
    if (parseInt($("#status").html()) == 0) {
        $("#notInGameText").html("Stats not available in lobby");
        currentStatus = "OFF";
    }
    if (parseInt($("#status").html()) == 1) {
        $("#notInGameText").html("Stats not available during a replay");
        currentStatus = "REPLAY";
    }
    if (parseInt($("#status").html()) == 2) {
        currentStatus = "LIVE";
    }
    if (parseInt($("#status").html()) == 3) {
        $("#notInGameText").html("Stats not available during pause menu");
        currentStatus = "PAUSE";
    }
    if (currentStatus == "LIVE")
        $("#notInGameDiv").hide();
    else {
        $("#notInGameDiv").show();
        return;
    }
    if (swipeInProgress)
        return;
    //SESSION INFO
    var sessionType = "Unknown";
    if (parseInt($("#sessionType").html()) == 0)
        sessionType = "Practice";
    else if (parseInt($("#sessionType").html()) == 1)
        sessionType = "Qualify";
    else if (parseInt($("#sessionType").html()) == 2)
        sessionType = "Race";
    else if (parseInt($("#sessionType").html()) == 3)
        sessionType = "Hot Lap";
    else if (parseInt($("#sessionType").html()) == 4)
        sessionType = "Time Attack";
    else if (parseInt($("#sessionType").html()) == 5)
        sessionType = "Drift";
    else if (parseInt($("#sessionType").html()) == 6)
        sessionType = "Drag";
    else
        sessionType = "Other";
    var sessionTimeLeft = parseFloat($("#sessionTimeLeft").html());
    var sessionTimeLeftObj = new Date(sessionTimeLeft);
    var seconds = sessionTimeLeftObj.getSeconds() > 9 ? sessionTimeLeftObj.getSeconds() : "0" + sessionTimeLeftObj.getSeconds();
    var minutes = sessionTimeLeftObj.getMinutes() > 9 ? sessionTimeLeftObj.getMinutes() : "0" + sessionTimeLeftObj.getMinutes();

    $("#sessionTypeAndTime").html(sessionType + " " + minutes + ":" + seconds);
    //PLAYER AND CAR INFO
    $("#playerNameDisplay").html($("#playerName").html());
    $("#carNameAndTrack").html(toTitleCase(replaceAll("_", " ", $("#carModel").html()) + " @ " + $("#trackName").html()));
    //PAGE 1
    if (currentPage == 1) {
        //TYRES
        var frontLeftTyreString = $("#frontLeftTyreInfo").html();
        var frontLeftTyreData = frontLeftTyreString.split("|");
        svgController.setTireInfo("lf", frontLeftTyreData);

        var frontRightTyreString = $("#frontRightTyreInfo").html();
        var frontRightTyreData = frontRightTyreString.split("|");
        svgController.setTireInfo("rf", frontRightTyreData);

        var backLeftTyreString = $("#backLeftTyreInfo").html();
        var backLeftTyreData = backLeftTyreString.split("|");
        svgController.setTireInfo("lr", backLeftTyreData);

        var backRightTyreString = $("#backRightTyreInfo").html();
        var backRightTyreData = backRightTyreString.split("|");
        svgController.setTireInfo("rr", backRightTyreData);

        //////////////////////////
        //DAMAGE
        var damageString = $("#damage").html();
        var damageData = damageString.split("|");
        var frontDamage = parseFloat(damageData[0]);
        var backDamage = parseFloat(damageData[1]);
        var leftDamage = parseFloat(damageData[2]);
        var rightDamage = parseFloat(damageData[3]);
        if (frontDamage != currentFrontDamage) {
            svgController.setDamagePercent("car_front", frontDamage / 100);
            currentFrontDamage = frontDamage;
        }
        if (backDamage != currentBackDamage) {
            svgController.setDamagePercent("car_back", frontDamage / 100);
            currentBackDamage = backDamage;
        }
        if (leftDamage != currentLeftDamage) {
            svgController.setDamagePercent("car_left", frontDamage / 100);
            currentLeftDamage = leftDamage;
        }
        if (rightDamage != currentRightDamage) {
            svgController.setDamagePercent("car_right", frontDamage / 100);
            currentRightDamage = rightDamage;
        }

        //TIMES
        $("#currentTimeValue").html("<p>" + $("#currentTime").html() + "</p>");
        $("#bestTimeValue").html("<p>" + $("#bestTime").html() + "</p>");
        $("#lastTimeValue").html("<p>" + $("#lastTime").html() + "</p>");
        //LAPS
        if ($("#totalLaps").html() == "0")
            $("#lapValue").html(" - \\ - ");
        else
            $("#lapValue").html(parseInt($("#completedLaps").html()) + 1 + " \\ " + $("#totalLaps").html());
        //POSITION
        $("#positionValue").html($("#position").html() + " \\ " + $("#totalCars").html());
    }
        //SECOND PAGE
    else {
        //SPEED, RPM & GEAR
        var newMaxRpm = parseInt($("#maxRpm").html());
        if (currentMaxRpm != newMaxRpm) {
            svgController.setMaxRpm(newMaxRpm);
            currentMaxRpm = newMaxRpm;
        }
        svgController.setSpeed(parseInt($("#speed").html()));
        svgController.setRPM(parseInt($("#rpm").html()));
        var newGear = parseInt($("#gear").html());
        if (currentGear != newGear) {
            svgController.setGear(newGear);
            currentGear = newGear;
        }
        //ODOMETER
        svgController.setOdometer(parseFloat($("#odometer").html()));
        //FUEL
        svgController.setFuel(parseFloat($("#fuel").html()));
        //SPLIT
        svgController.setSplit($("#split").html());
        //CURRENT TIME
        svgController.setCurrentTime($("#currentTime").html());
    }
}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}

var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
var isIPhone = (ua.match(/iphone/i) !== null && !isAndroid);
var isMiniAndroid = isAndroid && (ua.indexOf("mobile") != -1);

$(document).ready(function () {

    if ((isIPhone && window.innerWidth < 768) || isMiniAndroid || window.innerWidth < 700) {
        $("#layout").attr({ href: "styleSheetPhone.css" });
        $("#dashboardSVG").css("display", "none");
        $("#secondPage").hide();
    }
    else {
        $("#layout").attr({ href: "styleSheet.css" });
        $("#digitalDash").css("display", "none");
    }

    if (isMiniAndroid) {
        $("#speedText").css("font-size", "250px");
        $("#currentTimeLabel").css("font-size", "80px");
        $("#currentValue").css("font-size", "60px");
        $("#splitValue").css("font-size", "60px");
        if (window.devicePixelRatio >= 3) {
            $("#splitLabelText").css("font-size", "80px");
            $("#currentValue").css("font-size", "50px");
            $("#speedText").css("font-size", "200px");
        }
        else {
            $(".headerElement").css("font-size", "30px");
            $(".sessionInfoElementTextEven").css("font-size", "50px");
            $(".sessionInfoElementTextOdd").css("font-size", "50px");
            
        }
    }

    $("#notInGameDiv").hide();
    $(".pageDot").eq(0).css("background-color", dotColor);
    $("#properties").hide();
    $('#pageFrame').on('swiperight', function (event) {
            animateSwipe(1);
    });
    $('#pageFrame').on('swipeleft', function (event) {
        animateSwipe(2);
    });
    document.getElementById('abs_light').setAttribute('visibility', 'hidden');
    document.getElementById('abs_text').setAttribute('visibility', 'hidden');
    setInterval(update, 50);
    
});


