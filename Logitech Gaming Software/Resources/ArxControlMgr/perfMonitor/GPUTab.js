var tabModule = function(_tagName){
     //PRIVATE:
     var groupName = _tagName;
     var curPage = 0;
     var _numPages = 1;
     var tabBox =     $("#"+groupName);
     var tabContain = $("#"+groupName+'contain');
     var prefab =     $("#"+groupName+'prefab');
     var tabPips =    $("#"+groupName+"pips");
     tabPips.hide();
     var tabScroll =  $("#"+groupName+"scroll");
     $(window).resize( function(){
         setTimeout(function() { doScroll(0); }, 50);
     });

     var balanceLayout = function(){
          var tabs = tabContain.children("."+groupName+'tab');
          tabContain.width(tabs.length + "00%");
          for(var i =0; i < tabs.length; i++){
               tabs[i].style.width = (100 / tabs.length) + "%";
          }
          var allCounts = document.querySelectorAll("[id^='GPUCount']");
          for(var i=0; i < allCounts.length; i++){
               allCounts[i].innerText = ((i+1)+"/"+allCounts.length);
          }
     };
     var addTab = function(){
          _numPages++;
          var newTab = document.getElementById(groupName+'prefab').cloneNode(true);
          newTab.id = prefab.attr("id") + _numPages;
          tabContain.append(newTab);
          //Generate unique ids
          var namedChildren = newTab.querySelectorAll("[id]");
          console.log("#"+newTab.id + " , " + namedChildren.length);
          for (var i = namedChildren.length - 1; i >= 0; i--) {
               curChild = namedChildren[i];
               curChild.id = curChild.id+_numPages;
          }
          var d = document.createElement("div");
          tabPips.append(d);
          tabPips.show();
     };
//Set up events
     var startSwipeListen = function(){
          tabBox.on("swipeleft",function(){
               doScroll(1);
          });
          tabBox.on("swiperight",function(){
               doScroll(-1);
          });
          console.log("listening");
     };
     var stopSwipeListen = function(){
          tabBox.off("swipeleft");
          tabBox.off("swiperight");
          console.log("Stop listening");
     };
     var doScroll = function(direction){
          curPage+= direction;
          if(curPage >= _numPages) {curPage = _numPages-1;}
          if(curPage < 0){ curPage = 0;}
          var tabWidth = prefab.width();
          var newPos = tabWidth * curPage;
          tabScroll.animate(
               {scrollLeft:newPos}
          );
          console.log("Scrolling to " + newPos);
          $("#"+groupName+"pips > div").removeAttr("class"); 
          $("#"+groupName+"pips > div")[curPage].setAttribute("class","active");
     };

     //begin
     startSwipeListen();
     console.log("Loaded "+_tagName + "tabber");
     //PUBLIC module: 
     return {
          resizeTo: function(num){  while (_numPages < num)addTab(); balanceLayout(); },
          numPages: function(){ return _numPages; },
          curPage: function(){ return curPage; }
     };
};