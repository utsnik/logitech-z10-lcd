var parsedData;
var updateInterval;
var currentGameStatus = "DOTA_GAMERULES_NOT_IN_GAME";
var previousHeroLevel = 0;
var g_itemsData = undefined;
var g_currentItemsData = [];
var itemDescriptionTimeout;
var dotaBadgeShown = true;

String.prototype.replaceAll = function(str1, str2, ignore) 
{
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
}

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
} 

setTimeAndGold = function (totalSeconds, gold, GPM, XPM) 
{
	var parsedSeconds = 0;
	parsedSeconds = Math.abs(totalSeconds);
	var hours = Math.floor(parsedSeconds / 3600);
	parsedSeconds %= 3600;
	var minutes = Math.floor(parsedSeconds / 60);
	var seconds = parsedSeconds % 60;
	if(minutes < 10)
	{
		minutes = "0" + minutes;
	}
	if (seconds < 10)
	{
		seconds = "0" + seconds;
	}
	if(hours > 0)
	{
		$("#timeInGame").html(hours+":"+minutes+":"+seconds);
	}
	else
	{
		$("#timeInGame").html(minutes+":"+seconds);
	}
	$("#goldNumber").html(gold);
	if (GPM & XPM)
	{
	    $("#goldPerMinute").html("GPM: " + GPM);
	    $("#xpPerMinute").html("XPM: " + XPM);
	}
}

setProgressBar = function(progressBar, value, maxValue, percentage)
{
	if ((typeof value != 'undefined') && (typeof maxValue != 'undefined') && (typeof percentage != 'undefined'))
	{
		$("#"+progressBar+"ProgressbarProgress").css("width", percentage + "%");
		$("#"+progressBar+"Indicator").html(value+"/"+maxValue);	
	}
}

setHeroStats = function(playerName, heroName, kills, deaths, assists, lastHits, denies, killStreak)
{
	if ((typeof playerName != 'undefined') && (typeof heroName != 'undefined'))
	{
		$("#playerName").html(playerName);
		var heroParsed = heroName.substring(14);
		var heroParsedSpaced = heroParsed.replaceAll("_", " ");
		heroParsedSpaced = heroParsedSpaced.toUpperCase();
		$("#heroName").html(heroParsedSpaced);
		$("#killsTd").html(kills);
		$("#deathsTd").html(deaths);
		$("#assistsTd").html(assists);
		$("#lastHitsTd").html(lastHits);
		$("#DeniesTd").html(denies);
		$("#KillStreakTd").html(killStreak);
		var heroPicPath = "http://cdn.dota2.com/apps/dota2/images/heroes/"+heroParsed.toLowerCase()+"_vert.jpg"
		$("#heroPic").attr("src",heroPicPath);	
	}
}

updateRespawnOverlay = function(alive, respawnSeconds)
{
	if(!alive)
	{
		$("#countDownOverlay").fadeIn();
		$("#countDownText").html(respawnSeconds);
	}
	else
	{
		$("#countDownOverlay").fadeOut();
	}
}

updateHeroLevel = function(heroLevel)
{
	if(heroLevel > 0)
	{
		$("#heroLevel").show();
		$("#heroLevelText").html(heroLevel);
	}
	else
	{
		$("#heroLevel").hide();
	}
	if(previousHeroLevel != heroLevel)
	{	
	 	$("#heroImgContainer").effect("highlight", {}, 3000);
	}
	previousHeroLevel = heroLevel;
}

updateGameStatus = function (gameStatus)
{
	var popupText = "";
	if(gameStatus == "DOTA_GAMERULES_STATE_HERO_SELECTION")
	{
		popupText = "Selecting hero";
		showDotaBadge(popupText);
	}
	else if(gameStatus == "DOTA_GAMERULES_STATE_PRE_GAME")
	{
		popupText = "Pre game";
		hideDotaBadge();
	}
	else if(gameStatus == "DOTA_GAMERULES_STATE_GAME_IN_PROGRESS")
	{
		popupText = "Game in progress";
		hideDotaBadge();
	}
	else if(gameStatus == "DOTA_GAMERULES_STATE_POST_GAME")
	{
		popupText = "Post Game";
		hideDotaBadge();
	}
	else
	{
		popupText = "Enter a game to see stats";
		showDotaBadge(popupText);
	}

	currentGameStatus = gameStatus;

	$("#popupText").html(popupText);
}

updateItemDescription = function(currentItemData, itemId)
{

    $("#itemTitle").html((currentItemData.dname).toUpperCase());
    $("#itemTitle").removeClass();
    if (currentItemData.qual == "consumable")
    {
        $("#itemTitle").addClass("itemConsumable");
    }
    else if (currentItemData.qual == "component")
    {
        $("#itemTitle").addClass("itemComponent");
    }
    else if (currentItemData.qual == "secret_shop")
    {
        $("#itemTitle").addClass("itemComponent");
    }
    else if (currentItemData.qual == "common")
    {
        $("#itemTitle").addClass("itemCommon");
    }
    else if (currentItemData.qual == "rare")
    {
        $("#itemTitle").addClass("itemRare");
    }
    else if (currentItemData.qual == "artifact")
    {
        $("#itemTitle").addClass("itemArtifact");
    }
	$("#itemCost").html(currentItemData.cost);
	$("#itemDescription").html(currentItemData.desc);
	$("#itemAttribute").html(currentItemData.attrib);
	$("#itemLore").html(currentItemData.lore);
	$("#itemDescriptionBox").css('display', 'inline-block').hide().fadeIn();
	clearTimeout(itemDescriptionTimeout);
	itemDescriptionTimeout = setTimeout(function () {
                    $("#itemDescriptionBox").fadeOut();
                    $("#item"+itemId).removeClass('itemCellActive');
                }, 8000);
}

updateItems = function(itemsData)
{
	if (typeof itemsData != 'undefined' &&
		typeof itemsData.slot0 != 'undefined')
	{
		for(i=0; i<6; i++)
		{
			var itemData = eval("itemsData.slot"+i);
			if(itemData.name != "empty")
			{
				var itemName = itemData.name.replace("item_", "");
				var imageUrl = "http://cdn.dota2.com/apps/dota2/images/items/"+itemName+"_lg.png";
				$("#item"+i).html("<img src='"+imageUrl+"' class='itemImage'/>");
				g_currentItemsData[i] = g_itemsData.itemdata[itemName];
				$("#item"+i).unbind('click');
				$("#item" + i).bind('click', function () {
					var thisId = parseInt($(this).attr('id').replace("item",""));
					$(".itemCell").removeClass('itemCellActive');
					$(this).addClass('itemCellActive');
					updateItemDescription(g_currentItemsData[thisId], thisId);
				});
			}
			else
			{
			    $("#item" + i).html("<img src='empty_item.png' class='itemImage'/>");
				$("#item" + i).unbind('click');
			}
		}	
	}
}

update = function () {
	if(typeof g_itemsData == 'undefined')
	{
		parseItemData();
	}
	try
	{
	    var jsonData = JSON.parse($("#dataDiv").html());
    	if (jsonData != parsedData) {
    		if (typeof jsonData.map != 'undefined' &&
    			typeof jsonData.hero != 'undefined' &&
    			typeof jsonData.player != 'undefined')
    		{
    			if(jsonData.player.activity != "playing")
    			{
    				updateGameStatus("DOTA_GAMERULES_NOT_IN_GAME");
    			}
    			else
    			{
    				updateGameStatus(jsonData.map.game_state);
    			}
    			updateRespawnOverlay(jsonData.hero.alive, jsonData.hero.respawn_seconds);
				setProgressBar("health", jsonData.hero.health, jsonData.hero.max_health, jsonData.hero.health_percent);
				setProgressBar("mana", jsonData.hero.mana, jsonData.hero.max_mana, jsonData.hero.mana_percent);
				setTimeAndGold(jsonData.map.clock_time, jsonData.player.gold, jsonData.player.gpm , jsonData.player.xpm);
				setHeroStats(jsonData.player.name, jsonData.hero.name, jsonData.player.kills, jsonData.player.deaths, jsonData.player.assists, jsonData.player.last_hits, jsonData.player.denies, jsonData.player.kill_streak);
				updateHeroLevel(jsonData.hero.level);
				updateItems(jsonData.items);
    		}
			else
			{
				updateGameStatus("DOTA_GAMERULES_NOT_IN_GAME");
			}
			
			parsedData = jsonData;
    	}
		else
		{
			console.log("no new data received");
		}
	} 
	catch(e) 
	{
		console.log("no data received yet");
		updateGameStatus("DOTA_GAMERULES_NOT_IN_GAME");
	}
    
}

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


parseItemData = function ()
{
	g_itemsData = reloadJSON("itemsData.json");
}

showDotaBadge = function (textToDisplay)
{
	$("#dotaBadgeTxt").html(textToDisplay.toUpperCase());

	if(dotaBadgeShown)
	{
		return;
	}
	$("#dotaBadge").removeClass('dotaBadgeBottom');
	setTimeout(function () { $("#dotaBadgeLayer").fadeIn(500); }, 2000);
	dotaBadgeShown = true;	
}

hideDotaBadge = function ()
{
    $("#dotaBadgeTxt").html("");
	if(!dotaBadgeShown)
	{
		return;
	}
	$("#dotaBadgeLayer").fadeOut(1000, function() 
	{
	    $("#dotaBadge").addClass('dotaBadgeBottom');
	    dotaBadgeShown = false;
	});	
}

$(document).ready(function () {
    $(".hiddenDivs").hide();
	$("#countDownOverlay").hide();
	$("#heroLevel").hide();
	$("#itemDescriptionBox").hide();
	parseItemData();
    updateInterval = setInterval(function () { update(); }, 500);
    
    window.onorientationchange = function() { window.location.reload(); };
});

debug = function ()
{
	clearInterval(updateInterval);
	$("#popupOverlay").hide();
}