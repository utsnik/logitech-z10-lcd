var playerName = "";
var currentHealth = 0;
var currentArmor = 0;
var currentMoney = 0;
var currentKills = 0;
var currentAssists = 0;
var currentDeaths = 0;
var currentMvps = 0;
var currentScore = 0;
var currentTeam = "";
var numUpdatesWithoutTeam = 0;
var maxUpdatesWithoutTeam = 5;

$(document).ready(function () 
{
    $("#dataDiv").hide();
});

onPropertyUpdate = function () 
{
    playerName = $("#name").html();
    currentHealth = parseInt($("#health").html());
    currentArmor = parseInt($("#armor").html());
    currentMoney = parseInt($("#money").html());
    currentKills = parseInt($("#kills").html());
    currentAssists = parseInt($("#assists").html());
    currentDeaths = parseInt($("#deaths").html());
    currentMvps = parseInt($("#mvps").html());
    currentScore = parseInt($("#score").html());
    currentTeam = $("#team").html();
    $("#nameDiv").html(playerName);
    $("#killsCell").html(currentKills);
    $("#assistsCell").html(currentAssists);
    $("#deathsCell").html(currentDeaths);
    $("#mvpsCell").html(currentMvps);
    $("#scoreCell").html(currentScore);
    $("#moneyDiv").html("$ "+currentMoney);
    
    if (currentTeam == "T") 
    {
        $("#teamPic").show();
        $("#teamPic").css("background-image", "url('terrorist.png')");
        numUpdatesWithoutTeam = 0;
    }
    else if (currentTeam == "CT") 
    {
        $("#teamPic").show();
        $("#teamPic").css("background-image", "url('counter.png')");
        numUpdatesWithoutTeam = 0;
    }
    else 
    {
        numUpdatesWithoutTeam++;
        if(numUpdatesWithoutTeam > maxUpdatesWithoutTeam)
        {
            $("#teamPic").hide();    
        }
    }
    $("#healthProgressbarProgress").width(currentHealth+"%");
    $("#armorProgressbarProgress").width(currentArmor + "%");
}


