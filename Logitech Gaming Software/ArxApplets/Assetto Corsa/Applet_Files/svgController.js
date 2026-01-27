//
///////////////////////////////////////////////////////////////////////////////
///*----------------------------------------------------------------------------
///
///  Copyright (c) 2014 Logitech, Inc.  All Rights Reserved
///
///  This program is a trade secret of LOGITECH, and it is not to be reproduced,
///  published, disclosed to others, copied, adapted, distributed or displayed
///  without the prior authorization of LOGITECH.
///
///  Licensee agrees to attach or embed this notice on all copies of the program,
///  including partial copies or modified versions thereof.
///
//--------------------------------------------------------------------------*/
/// svgController - This object provides methods to set attributes and properties of the Asseto Corsa Arx Control applet
///
///  Author: Tiziano Pigliucci
///  Date: 5/20/2014
///////////////////////////////////////////////////////////////////////////////
// 
// Methods:
// setMaxRpm(maxRpm) - Sets the tachometer range for the tac dial and colors the non critical tics gray
//    integer maxRpm - the maximum range for the RPM (0 - 12000)
//
//  SetFuel(fuel) - Sets the fuel percentage on the fuel gauge indicator.  If the fuel is less than 10% the method also 
//                  lights the fuel indicator lamp
//     integer fuel - the percentage of to sent the fuel indicator (0 - 100)
//
//  setAbsOn (isOn) - Sets the ABS indicator on or off
//		boolean isOn - The indicator status true = on : false = off
//
//	setOdometer(km) - Sets the odometer text to the value specified in the string km
//		string km - a formatted string with the odometer value ('123.1') for example
//
//  setGear(gear) - Sets the current gear indicator
//		integer gear - The current gear (0=reverse, 1= neutral, 2-n = the gear value - 2)
//						 Example: svgController.setGear(3) will display the gear as "1"
//
//	setRPM(rpm) - Sets the rpm needle to the correct value based on the passed in argument
//		integer rpm - The rpm value between (0 and maxRPM (currently 12000))
//
//	setSpeed(speed) - Sets the speed needle to the correct value based on the passed in argument
//		integer speed - The speed value between (0 and maxSpeed (currently 360))
//
//
//	setSplit(split) - Sets the split text in the iPhone layout to the correct value based on the passed in argument
//		string speed - The split value
//
//
//	setCurrentTime(currentTime) - Sets the current time text in the iPhone digital dashboard
//		string currentTime - The current time as a string to be set in the digital dashboard
//
//	setDamagePercent(region, damagePercent) - Sets the percentage of damage on the indicated car region (quadrant)
//		string region - a member of the set {'car_front','car_back','car_left','car_right'}
//		float damagePercent - the amount of damage to the region as a number between 0.0 and 1.0 
//							  (0 is undamaged and 1.0 is total damage)
//
//	setTireInfo(tire, info) - Sets the information for each tire box
//		string tire - a member of the set {'lf','rf','lr','rr'}
//		float[] info - An array of values for each tire. The array indexes must match the line_n positions in the SVG
//
var svgController = {
    tickRed :'#800000',
	tickGray : '#ccc',
	indicatorOn : '#990000',
	indicatorOff : '#2b0000',
	fuelWarningLevel : 10,
	minFuel : 0,
	MaxFuel : 100,
	totalRpmTics : 12,
    currentMaxRpm : 0,
    "setMaxRpm": function (maxRpm)
    {
        if (!(isIPhone || isMiniAndroid)) {
            var maxTick = Math.floor(maxRpm / 1000);
            for (var i = this.totalRpmTics; i > (maxTick - 1) ; i--) {
                document.getElementById('t' + i).setAttribute('visibility', 'hidden');
            }
            for (var i = 0; i <= maxTick + 1; i++) {
                document.getElementById('t' + i).setAttribute('visibility', 'visible');
            }
            for (var i = 0; i <= (maxTick - 1) ; i++) {
                document.getElementById('t' + i).style.stroke = this.tickGray;
                document.getElementById('t' + i).style.fill = this.tickGray;
            }
            document.getElementById('t' + maxTick).style.stroke = this.tickRed;
            document.getElementById('t' + maxTick).style.fill = this.tickRed;
            document.getElementById('t' + (maxTick - 1)).style.stroke = this.tickRed;
            document.getElementById('t' + (maxTick - 1)).style.fill = this.tickRed;
            document.getElementById('t' + (maxTick + 1)).style.stroke = this.tickRed;
            document.getElementById('t' + (maxTick + 1)).style.fill = this.tickRed;
        }
        else {
            document.getElementById('maxRpmText').textContent = maxRpm;
        }

        currentMaxRpm = maxRpm;
    },
    "setFuel": function (fuel) {
        //
        // Sanity check the inbound parameter and normalize
        if (fuel < this.minFuel)
        {
            fuel = this.minFuel;
        }
        else if (fuel > this.maxFuel)
        {
            fuel = this.maxFuel;
        }
        if ((isIPhone || isMiniAndroid)) {
            var maskHeight = 296.38;
            var newMaskHeight = maskHeight - maskHeight * fuel / 100;
            document.getElementById('fuelVertMask').setAttribute('height', parseInt(newMaskHeight));
        }
        else {
            var maskWidth = 104.89;
            var maskX = 146.58;
            var newMaskWidth = maskWidth - maskWidth * fuel / 100;
            document.getElementById('fuelMask').setAttribute('width', parseInt(newMaskWidth));
            document.getElementById('fuelMask').setAttribute('x', parseInt(maskWidth * fuel / 100) + maskX);
            if (fuel < this.fuelWarningLevel)
                document.getElementById('low_fuel_light').style.fill = this.indicatorOn;
            else
                document.getElementById('low_fuel_light').style.fill = this.indicatorOff;
        }
    },
    "setAbsOn": function (isOn) {
        document.getElementById('abs_light').style.fill = isOn ? this.indicatorOn : this.indicatorOff;
    },
    "setOdometer": function (km) {
        var kmStr = "";
        if (km == Math.floor(km))
            kmStr = km + ".0";
        else
            kmStr = km;
        document.getElementById('odometer_text').textContent = kmStr;
    },
    "setGear": function (gear) {
        var gearText = "";
        if (gear == 0)
            gearText = "R";
        else if (gear == 1)
            gearText = "N";
        else
            gearText = --gear;
        var element = !(isIPhone || isMiniAndroid) ? 'gearText' : 'gearTextPhone';
        document.getElementById(element).textContent = gearText;

    },
    "setRPM": function (rpm) {
        if (rpm < 0)
            return;
        if ((isIPhone || isMiniAndroid)) {
            document.getElementById('rpmText').textContent = rpm;
            var maskWidth = 667.89;
            var maskX = 35.4;
            var rpmPercentage = rpm / currentMaxRpm;
            var newMaskWidth = maskWidth - maskWidth * rpmPercentage;
            document.getElementById('rpmMask').setAttribute('width', parseInt(newMaskWidth));
            document.getElementById('rpmMask').setAttribute('x', parseInt(maskWidth * rpmPercentage) + maskX);
        }
        else {
            var rpmRadiant = (22.5 * (rpm / 1000));
            document.getElementById('tac_needle_rotate').setAttribute("transform", "rotate(" + rpmRadiant + ", 362.25, 213.531)");
        }


    },
    "setSplit": function (split) {
        //this only applies to the iPhone layout
        if (!(isIPhone || isMiniAndroid))
            return;
        document.getElementById('splitValue').textContent = split;
    },
    "setCurrentTime": function (currentTime) {
        //this only applies to the iPhone layout
        if (!(isIPhone || isMiniAndroid))
            return;
        document.getElementById('currentValue').textContent = currentTime;
    },
    "setSpeed": function (speed) {
        if ((isIPhone || isMiniAndroid)) {
            document.getElementById('speedText').textContent = speed;
        }
        else {
            var speedRadiant = (30 * speed / 40);
            document.getElementById('speed_needle_rotate').setAttribute("transform", "rotate(" + speedRadiant + ", 31.25, 213.416)");
        }

    },
    "setDamagePercent": function (region, damagePercent) {
        var svgObject;
        switch (region) {
            case 'car_front':
            case 'car_back':
            case 'car_left':
            case 'car_right':
                svgObject = document.getElementById(region);
                if (svgObject) {
                    svgObject.style.opacity = damagePercent;
                }
                break;
            default:
                alert('You did not specify a correct damage region');
        }
    },
    "setTireInfo": function (tire, info) {
        var textElement;
        switch (tire) {
            case 'lf':
            case 'rf':
            case 'lr':
            case 'rr':
                var index;
                for (index = 1; index <= info.length; ++index) {
                    var label = tire + '_line' + index;
                    textElement = document.getElementById(label);
                    if (textElement) {
                        textElement.textContent = info[index - 1];
                    }

                }
                break;
            default:
                alert('You did not specify a correct tire location, try one of these [lf,rf,lr,rr]');
        }
    }
};

var damagePercent = 0.90;
var testTireInfo = [454.12, 321.12, 321.12, 321.12, 321.12];