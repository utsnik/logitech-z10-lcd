
var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
var isiPhone = (ua.match(/iphone/i) !== null && !isAndroid && window.innerWidth<737);
var isMiniAndroid = isAndroid && ( (ua.toLowerCase().indexOf("mobile") != -1) || (ua.toLowerCase().indexOf("nexus 5") != -1 ));
var localizedStrings;

Array.prototype.average = function () {
    var sum = 0, j = 0;
   for (var i = 0; i < this.length, isFinite(this[i]); i++) {
          sum += parseFloat(this[i]); ++j;
    }
   return j ? sum / j : 0;
};
Properties= function(values_, max_, maxTag_){
	this.values = values_;
	this.max	= max_;
	this.maxTag = maxTag_;
};
var parseProperties = function (tagName){
	var values = $("#"+tagName).text();
	var max= -1;
	var maxTag = "";
	if(values.indexOf("|")!== -1)
	{
		valueArr = values.split("|");
		var maxString = valueArr.pop();
		max = parseFloat(maxString);
		maxTag = maxString.replace(max,"");
		values = valueArr.join("|");
	}
	values = values.split(",");
	return new Properties(values, max, maxTag);
};
//Add this back in before barBack to add temperatures.
//<span class="barTop">$VALUE</span>
var barPrefab = '<li class="barContainer"><span class="barBack"><span class="barFill"></span></span><p class="barPcent">$PERCENT</p></li>';

var onPropertyUpdate = function () {
	renderCPU();
	renderGPU();
	renderRAM();
	if (typeof miniApplet !== 'undefined') {
		miniRedistribute();
	}
	else{
		fullRedistribute();
	}
};

var resizeCoresTo = function(numBars){
	//create or remove tags until we have one for each value
	var i = 32;  //Failsafe if parsing failed spectacularally
	var tags = [];

	while( i-- ){
		tags = $("li", "#CPUTemps");
		if(tags.length < numBars){
			$("#CPUTemps").append(barPrefab);
		}
		else if(tags.length > numBars){
			$("li", "#CPUTemps").last().remove();
		}
		else{
			break;
		}
	}
	return tags;
};

var genSuffixes= function(numTabs){
	var suffixes = [""];
	for(var i=1; i < numTabs; i++){
		suffixes.push( ""+(i+1));
	}
	return suffixes;
};

var renderValue = function(tag){
	var properties = parseProperties(tag);
	var suffixes = genSuffixes(properties.values.length);
	for(var i=0; i < suffixes.length; i++){
		var avg = properties.values[i];
		var t = avg / properties.max;
		var bar = $("#" + tag + "B"+suffixes[i]);
		var txt = $("#" + tag + "v"+suffixes[i]+", #alt" + tag + "v"+suffixes[i]);
		var displaySupported = avg >= 0;
		if(txt){
			txt.css("display", displaySupported?"inherit":"none");
			txt.text(avg + properties.maxTag);
		}
		if(bar){
			bar.css("display", displaySupported?"inherit":"none");
			bar.css("width", (t * 100) + "%");
			bar.css("background-color", heatmapColor(t));
		}
	}
};

var renderCPU = function(){
	var cpuTemp = parseProperties("CPUTemp");
	var cpuUsage = parseProperties("CPUUsage");
	var totalUsage = cpuUsage.values.average();
	var totalTemp = cpuTemp.values.average();

	//fullsize Applet
	if (typeof miniApplet === 'undefined') {
		var coreBars = resizeCoresTo(cpuUsage.values.length);
		for (var i = coreBars.length - 1; i >= 0; i--) {
			var core = coreBars[i];
			var temp = cpuTemp.values[i] || 0;
			var hScale = 0.7;
			if(window.innerWidth > window.innerHeight ){ hScale = 0.5; }
			if (isiPhone || isMiniAndroid) {
			    hScale *= 0.6;
			}
			$(core).children(".barBack").css("height", ($("#CPU").height()* hScale) - 20 + "px");
			var percentString = cpuUsage.values[i];
			//Add a % if we have room
			if (coreBars.length <= ((isiPhone || isMiniAndroid) ? 8 : 16) ) {
				percentString += cpuUsage.maxTag;
			}
			$(core).children(".barPcent").text(percentString);
			core.style.width = 80 / coreBars.length + "%";
			core.style['margin-left'] = 15 / coreBars.length + "%";
			if(cpuUsage.max !== -1)
			{
				var t = parseFloat(cpuUsage.values[i]) / cpuUsage.max;
				var bar =$(core).find(".barFill");
				bar.css( "height",  ((t * 100)) + "%");
				$(core).find(".barFill").css( "background-color",  heatmapColor(t) );
			}
		}
		//temp icon:
		var temp = parseFloat($("#CPUTempv").text());
		var tempBounds = [62,69,75,200];
		var tempNames = ["Green", "Yellow", "Red", "Blink"];

        var tempColors = ["#0f0", "#fF0","#f00","#f00"];
		for(var j=0; j< tempBounds.length; j++){
			if(temp < tempBounds[j]){
				document.getElementById("CPUTempBlock").className = "tempIcon"+tempNames[j];
				document.getElementById("CPUTempBlock").style.color = tempColors[j];
				break;
			}
		}
		temp = parseInt((temp * 1.8) + 32);
		$("#CPUTempF").html(temp+'&deg;F');
	}
	else{
		//mini applet
		//we can only display one value at a time.
		$("#CPUUsageB").css("width", (totalUsage / cpuUsage.max) * 100 + "%");
	}
	$("#CPUUsagev").text(totalUsage.toFixed(2) + cpuUsage.maxTag);
	//$("#CPUTempv").text(totalTemp.toFixed(0) + " " + cpuTemp.maxTag);
};

var renderGPU = function () {


    var usageDestination = "";
    //Add new tabs if necessary

	//update bars and text
    ["GPUTemp", "GPUUsage", "GPUClockSpeed", "GPUFanSpeed"].forEach(renderValue);
	if($("#NvidiaBlock").is(":visible"))
	{
		["FrameBuffer","VideoEngine","BusInterface","GPUMemory"].forEach(renderValue);
		usageDestination = "#NVIDIATable";
	}

	else if($("#ATIBlock").is(":visible")){
		["EngineClock","MemoryClock","GPUVoltage"].forEach(renderValue);
		usageDestination = "#ATITable";
	}

    var suffixes = [""];
	if (typeof miniApplet === 'undefined') {
		GPUTabModule.resizeTo($("#numGPU").text());
		suffixes = genSuffixes(GPUTabModule.numPages());

	//do per-tab updates
	for(var i=0; i < suffixes.length; i++){
		var sf = suffixes[i];
		//grab usage and temperature bars
		var elem = $("#usageBlock"+sf ).detach();
		elem.prependTo(usageDestination +sf+" > tbody");
		//temperature
		var temp = parseFloat($("#GPUTempv"+sf).text());
		// Remove any decoration first
		$("#GPUTempv"+sf).html(temp+'&deg;C');
		//temp icon:
		var tempBounds = [70,85,100,110];
		var tempNames = ["Green", "Yellow", "Red", "Blink"];

        var tempColors = ["#0f0", "#fF0","#f00","#f00"];
		for(var j=0; j< tempBounds.length; j++){
			if(temp < tempBounds[j]){
				document.getElementById("GPUTempBlock"+sf).className = "tempIcon"+tempNames[j];
				document.getElementById("GPUTempBlock"+sf).style.color = tempColors[j];
				break;
			}
		}
		//temp translation
		temp = parseInt((temp * 1.8) + 32);
		$("#GPUTempF"+sf).html(temp+'&deg;F');
		}
	}

};

var renderRAM = function(){
	var ramData = parseProperties("RAMUsage");
	var used = ramData.values[0];
	var total = ramData.max;
	$("#RAMFree").text(used + ramData.maxTag );
	$("#RAMTotal").text(total + ramData.maxTag );
	genPie( 100-((total - used) / total)*100 );
};

//Rotate and resize the #piechart div.
var genPie = function(percent){

	var chart = $("#piechart");
	var wedge = chart.find(".pie");
	var hold = chart.find(".hold");
	rotation = ((360 * percent)/100) % 180;
	var majorColor = "#666";
	var minorColor = "#00A0D0";
	//swap pie pieces, the rotation trick only works with values < 50%
	if(percent >= 50){
		var temp = minorColor;
		minorColor = majorColor;
		majorColor = temp;
		rotation = 180 - rotation;
		hold.css("transform", "rotate("+(-rotation)+"deg)");
	}
	else{
		hold.css("transform", "rotate(0deg)");
	}
	chart.css("background-color",majorColor);
	wedge.css("background-color", minorColor);
	wedge.css("transform", "rotate("+rotation+"deg)");
	chart.find("span").text(Math.round(percent) + "%");
};

var resizePie = function () {
    if (typeof miniApplet == 'undefined') {
        var ramName = "#ramPieTableCell";
    } else {
        var ramName = "#RAM";
    }
    if (typeof miniApplet == 'undefined') {
        var scale = 0.6;
    } else {
        scale = 0.7;
        if (isAndroid)
            scale = 0.6;
    }

	var width = Math.min($(ramName).width(),$(ramName).height()) * scale;

	var chart = $("#piechart");
	var wedge = chart.find(".pie");
	var hold = chart.find(".hold");
	var full = width+"px";
	var half = (width/2)+"px";
	//chart.parent().css("width", full);
	chart.css("width", full);
	chart.css("height", full);
	wedge.css("width", full);
	wedge.css("height", full);
	wedge.css("border-radius", half);
	wedge.css("clip", "rect(0px,"+half+","+full+",0px)");
	hold.css("clip", "rect(0px,"+full+","+full+","+half+")");
	chart.find("span").css("font-size", (width/3) + "px");
	chart.find("span").css("padding-top", (width/6) + "px");
};

//Reorganizes the blocks for iPhone vs iPad
var miniRedistribute = function(){
	var gpuShown = $("#GPU").css("display") != "none";
		//[cpu][gpu][ram]
		$("#CPU").css("width", gpuShown?"33%":"50%");
		$("#GPU").css("width", gpuShown?"33%":"0");
		$("#RAM").css("width", gpuShown?"34%":"50%");
		resizePie();
};

var itoH = function(i){
	var hex = Number(i).toString(16);
    while (hex.length < 2) {
        hex = "0" + hex;
    }
    return hex;
};

var heatmapColor = function( t ){
	var max = [244,4,16];  //F40410
	var mid = [255, 233, 1]; //FFE901
	var min = [1, 219, 11]; //

	t=t*t;
	if(t < 0.5){
		max = mid;
	}
	else{
		min = mid;
		t -= 0.5;
	}
	t = t * 2;
	var r = parseInt(min[0] + (max[0] - min[0]) * (t));
	var g = parseInt(min[1] + (max[1] - min[1]) * (t));
	var b = parseInt(min[2] + (max[2] - min[2]) * (t));
	return "#" + itoH(r) + itoH(g) + itoH(b);
};

var fullRedistribute = function(){
	var pi = $("#piechart");
		var gpuShown = $("#GPU").css("display") != "none";

    if (window.innerWidth > window.innerHeight) {
        //[   cpu  ]
        //[gpu][ram]
		console.log("landscape");

		/*
		$("#GPU").css("width" , "45%");
		$("#RAM").css("width" ,  gpuShown ? "45%" : "94%");

		$("#CPU").css("height" ,  "40%");
		$("#GPU").css("height" ,  "48%");
		$("#RAM").css("height" ,  "48%");
		*/

		$("RAMf").css("float","left");
		$("#RAMcontainer").css("font-size", "");
		$(".GPUBadges h3").css("font-size", "100%");
		$(".GPUBadges h3").css("margin", "0 3%");

		$(".CPUBadges h3").css("font-size", "100%");
		$(".CPUBadges h3").css("margin", "0 3%");
	}
    else {
        //[cpu]
        //[gpu]
        //[ram]
		/*$("#GPU").css("width" , "94%");
		$("#RAM").css("width" , "94%");

		$("#CPU").css("height" , "30%");
		$("#GPU").css("height" , "36%");
		$("#RAM").css("height" , "24%");*/

		$("#RAM").css("overflow", "hidden");
		$("#RAM").css("clear","none");
		$("RAMf").css("float", "right");

		if (isiPhone) {
		    $(".GPUBadges h3").css("font-size", "150%");
		    $(".GPUBadges h3").css("margin", "0% 3%");

		    $(".CPUBadges h3").css("font-size", "150%");
		    $(".CPUBadges h3").css("margin", "0% 3%");
		}
		if (isMiniAndroid) {
		    $(".GPUBadges h3").css("margin", "0% 3%");
		    $(".GPUBadges h3").css("font-size", "90%");

		    $(".CPUBadges h3").css("margin", "0% 3%");
		    $(".CPUBadges h3").css("font-size", "90%");

		    $(".GPUTable").css("font-size", "90%");
		    $(".GPUTable").css("height", "60%");
		}
		if (!isiPhone && !isMiniAndroid) {
		    $("#RAMcontainer").css("font-size", "150%");
		    $(".GPUBadges h3").css("font-size", "125%");
		    $(".GPUBadges h3").css("margin", "0% 3%");

		    $(".CPUBadges h3").css("font-size", "125%");
		    $(".CPUBadges h3").css("margin", "0% 3%");

		    $(".gpuBlock").css("height", "80%");
		}
	}

	var hScale = 0.7;
	if(window.innerWidth > window.innerHeight ){ hScale = 0.5; }
	if(isiPhone || isMiniAndroid){ hScale *= 0.6;}
	$(".barBack").css("height", $("#CPU").height() * hScale + "px");
	resizePie();

};

var onACBridgeLoad = function(){

    //ACBridge.trLoadStrings();
    //ACBridge.trAll();
    htmlInit();
};

$(document).ready(function () {
    if (typeof miniApplet != 'undefined' && isAndroid) {
        $("body").css("font-size", "0.6em");
        $("h2").css("margin-right", "0");
    }
	  var tempVisible=false;
	$('#CPUTempC').bind("DOMSubtreeModified",function(){
	    var temp = parseFloat($("#CPUTempv").text());
		if (tempVisible==false && temp!=0.0)
		{
			$("#CPUTempC").show();
			tempVisble=true;
		}
	});
    $("#CPUTempF").hide();
	$("#CPUTempC").hide();
});
