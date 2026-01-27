skew = 100/32.0

with open("ColorMap.txt", 'w') as f:
	f.write( "#Map to device\n" )
	for g in range(0,256):
		gMod = g;
		toF = (g / 255.0 );
		gMod = 1 - (1- toF)** ( skew );
		gMod *= 255
		f.write( str(int(gMod))  +"\n")


	f.write( "#Map from device\n" )
	for g in range(0,256):
		gMod = g;
		toF = (g / 255.0 );
		gMod =  1 - (1- toF)** ( 1/skew );
		gMod *= 255
		f.write( str(int(gMod))  +"\n")