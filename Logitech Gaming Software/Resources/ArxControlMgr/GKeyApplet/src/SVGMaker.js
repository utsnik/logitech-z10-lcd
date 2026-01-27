var svgNS = "http://www.w3.org/2000/svg";
var lnkNS = "http://www.w3.org/1999/xlink";
var svg;
var defs;
var img;
var pathnum = 0;
var zooming = 2;

var setupSVG = function () {
    $("#svgView").remove();
    svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("xmlns",svgNS);
    svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", lnkNS);
    //svg.setAttribute('style', 'border: 1px solid black');
    svg.setAttribute("id", "svgView");
    document.getElementById('gView').appendChild(svg);
};

var resetSVG = function(newImage){
    var h = newImage.height;
    var w = newImage.width;

    var zoomW = 1, zoomH = 1, zoomN;
    var gViewW = $("#gView").width(), gViewH = $("#gView").height();

    if (w > gViewW) {
        zoomW = Math.ceil(w / gViewW);
    }
    if (h > gViewH) {
        zoomH = Math.ceil(h / gViewH);
    }
    zoomN = (zoomW > zoomH) ? zoomW: zoomH;
    zoomN = (zoomN > 2) ? zoomN: 2;

    document.getElementById('gView').removeChild(svg);
    $("#svgView").remove();
    setupSVG();

    /*
    svg.setAttribute('data-basewidth', w);
    svg.setAttribute('data-baseheight', h);
    */
    $("#svgView").attr('data-basewidth', w);
    $("#svgView").attr('data-baseheight', h);

    /*svg.setAttribute('width', w+"px");
    svg.setAttribute('height', h+"px");
    var maxW = Math.max(window.innerWidth, w);
    var maxH = Math.max($("#gView").height(), h);*/

    var numX = (isNaN($("#gView").x)) ? 0: $("#gView").x;
    var numY = (isNaN($("#gView").y)) ? 0: $("#gView").y;

    //svg.setAttribute('viewBox',
    //    (parseInt($("#gView").width() / 2) - parseInt((w * zoomN) / 2) + numX) + ' ' +
    //    (parseInt($("#gView").height() / 2) - parseInt((h * zoomN) / 2) + numY)+' ' +
    //    (w * zoomN) + ' ' + (h * zoomN)
    //);

    defs = document.createElementNS(svgNS, "defs");
    svg.appendChild(defs);
    img = document.createElementNS(svgNS, "image");
        img.setAttributeNS(lnkNS, "href", devImage.src);

        img.setAttribute("width", w+"px");
        img.setAttribute("height", h+"px");

        img.setAttribute("id", "svgImage");
        img.setAttribute("y",0);
        img.setAttribute("x",0);

    svg.appendChild(img);
    pathnum = 0;
    $("#svgView").css("width", $("#svgImage").attr("width"));
    $("#svgView").css("height", $("#svgImage").attr("height"));
};
var makeText = function(word, x,y,w,h){
    var txt = document.createElementNS(svgNS, "text");
    txt.setAttributeNS(null, "fill", "white");

    p = document.createElementNS(svgNS, "path");
    pathnum ++;
    p.setAttributeNS(null, 'id', "P"+pathnum);
    p.setAttributeNS(null, "d", "M " + (x+5) + " " + (y+h*0.8) + " h " + (w - 10) );
    defs.appendChild(p);
    var phrase = document.createElementNS(svgNS,"textPath");
    
    phrase.setAttributeNS(lnkNS,"href", "#P"+pathnum);
    phrase.setAttributeNS(null, "class", "textpath");
    
    phrase.appendChild(document.createTextNode(word));
    txt.appendChild(phrase);
    svg.appendChild(txt);
    var bbox = txt.getBBox();
    //set if we have a small text box
    if(bbox.width < w * 0.8){
        txt.setAttributeNS(null, "text-anchor","middle");
        phrase.setAttributeNS(null,"startOffset","50%");
        console.log(word + " " + bbox.width + " < " + (w * 0.8));
    }
};

var makeRect = function(x,y,w,h,color){
    var rect = document.createElementNS(svgNS, "rect");
    rect.setAttributeNS(null,'x',x);
    rect.setAttributeNS(null,'y',y);
    rect.setAttributeNS(null,'width',w);
    rect.setAttributeNS(null,'height',h);
    rect.setAttributeNS(null,'fill',color);
    rect.setAttributeNS(null,'rx',3);
    rect.setAttributeNS(null,'ry',3);
    rect.setAttributeNS(null,'fill-opacity',0.8);
    rect.setAttributeNS(null, 'stroke', "white");

    rect.setAttributeNS(null,'stroke-width','1');
    svg.appendChild(rect);
};
var makeLine = function(x,y,x2,y2){
    console.log("This is a line");
    var line = document.createElementNS(svgNS, "line");
    line.setAttributeNS(null, "x1",x);
    line.setAttributeNS(null, "y1",y);
    line.setAttributeNS(null, "x2",x2);
    line.setAttributeNS(null, "y2",y2);
    line.setAttributeNS(null, "stroke", "white");
    line.setAttributeNS(null, "stroke-width","4");
    svg.appendChild(line);

};

var makeTextBox = function(word, x,y,w,h,w2){
//    makeRect(x,y,w2,h, "blue");
    if(word !== ""){
        makeRect(x,y,w,h, "gray");
        makeText(word, x,y,w,h);
    }
};
var findTag = function(list,id){
    for(i=0; i < list.length; i++){
        if(list[i].contextID == id)
            return list[i].macroName;
    }
    return "";
};