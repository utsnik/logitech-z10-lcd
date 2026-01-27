var curDeviceVersion = -4;
var curProfileVersion = -4;
var connectedDevices = 0;
var tagList;
var tagValues;

var truncate = function(string, len)
{
    ret = string;
    if(ret.length > len )
    {
        ret = ret.substring(0,len);
        ret+= "...";
    }
    return ret;
}
var getDevIndex=function(){
    if (typeof localStorage.deviceIndex === 'undefined') {
        localStorage.deviceIndex = 0;
    }
    //If we connect to a different computer with a different number of devices
    if(localStorage.deviceIndex > connectedDevices -1){
        localStorage.deviceIndex = 0;
    }
    console.log("returning device index >"+parseInt(localStorage.deviceIndex)+"<");
    return parseInt(localStorage.deviceIndex);
};

var setDevIndex= function(i){
    if(i < 0) { i = 0;}
    localStorage.deviceIndex = i;
    localStorage.activeDevice = tagList[i].device;
    console.log("setting device index to >"+parseInt(localStorage.deviceIndex)+"<");
    return parseInt(localStorage.deviceIndex);
};
var stepDevice = function(dir){
    var di = getDevIndex() + dir;
    if(di < 0){ di = tagList.length-1;}
    di = di% tagList.length;
    setDevIndex(di);
    renderProfile();
    renderDeviceList();
};


var startLoadDevImage = function(){
    /*$(".devicePic").css('background-image', "url('img/loading.gif')");*/
    var di = getDevIndex();
    loadingInterval = setTimeout(function () { loadImageTimeout($(".devicePic"), tagList[di]["image"] + ".png"); }, 200);
    devName = truncate(devName, 20);
    $(".deviceName").text(devName);
    loadDeviceImage(tagList[di]["image"]);
};
var parseInit = function () {
    if(typeof tagList === 'undefined'){tagList = {};}
    if (typeof tagValues === 'undefined') { tagValues = {}; }

    if(typeof renderDeviceList === 'undefined'){
        renderDeviceList = function(){
            console.log("Did not assign renderDeviceList yet");
        };
    }

    if(typeof renderProfile === 'undefined'){
        renderProfile = function(){
            console.log("Did not assign renderProfile yet");
        };
    }
};

var reloadJSON = function(src) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", src, false);
        xmlhttp.send();
        var ret;
	    try {
	        ret = JSON.parse(xmlhttp.responseText);
	    }catch(e){
            console.warn("Could not load json: " + src);
        }
        return ret;
};

var onPropertyUpdate = function () {
    console.log("On property update from "+window.location.href);
		//only need to update if the device list changed
		var newDevVersion = $("#deviceVersion").text();
		var newProfileVersion = $("#activeProfile").text();

		if(newDevVersion > curDeviceVersion || newProfileVersion > newDevVersion)
		{
			tagList = reloadJSON("device_assignment_labels.js");
			tagValues = reloadJSON("device_assignments.js");
            connectedDevices = tagList.length;
		}

		if(newDevVersion > curDeviceVersion)
		{
			curDeviceVersion = newDevVersion;
			renderDeviceList();
		}

		if( newProfileVersion != curProfileVersion)
		{
		    //ACBridge.log("profile version changed");
			curProfileVersion = newProfileVersion;
			renderProfile();
		}
};

var findDevice = function(json, device){
		for (var i = json.length - 1; i >= 0; i--) {
			if(json[i].device == device){
				return json[i];
			}
		}
		ACBridge.log("Couldn't find device >" + device +"<");
		return null;
};


var onACBridgeLoad = function(){
    ACBridge.trLoadStrings();
    ACBridge.trAll();
    parseInit();
    if ((isiPhone || isMiniAndroid) && (document.URL.indexOf("_small") == -1)) {
        window.location.href = "index_small.html";
        console.log("Window is small!");
    }
    onPropertyUpdate();
    renderInit();
};
