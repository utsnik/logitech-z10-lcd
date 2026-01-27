glyphsize=32
while getopts "fghkrs:" opt; do
  case $opt in
    f)
      forcing=true
	  if [ -n "$replacing" ];
	  then
		echo "Cannot use -f and -r at the same time" >&2
		exit 1
	  fi
      ;;
    g)
      gkeys=true
      ;;
	h)
	  echo "Usage:\n -h: Display help \n -f: force re-parse \n -g: Do g-keys in range (1-max) \n -k [max=10]" >&2
	  exit
      ;;
    k)
      mainkeys=true	  
      ;;
	r)
	  replacing=true
	  if [ -n "$forcing" ];
	  then
		echo "Cannot use -f and -r at the same time" >&2
		exit 1
	  fi
	  ;;
	s)
	  glyphsize=$OPTARG
	  ;;
    \?)
	  echo "Usage:\n -h: Display help \n -f: force re-parse \n -g: Do g-keys \n -k Do main keyboard \n -r: re-render glyphs (don't blindly search) \n -s: size of the glyph width" >&2
	  exit 1
	  ;;
  esac
done

echo "Gkeys is $gkeys Mainkeys is $mainkeys Forcing is $forcing Replacing is $replacing glyph size is $glyphsize"

for f in `ls Svg/`
do
	lang=`expr "$f" : 'G910_\(.*\)\.'`
	if [ -n "$forcing" ]; then
		echo "I'd remove >$lang< here"
		#rm -f $f 
	fi
	
	mkdir -p $lang
	mkdir -p "${lang}ref"
	echo "Svg/$f"
	for i in {4..255}
	do
		curLetter="Letter_0x$(printf "%02x" $i)"
		outfile="$PWD/$lang/$curLetter.png"
		if [ -z "$replacing" ] || [ -e $outfile ]
		then
			"/c/Program Files (x86)/Inkscape/inkscape.com" -z -f "Svg/$f" -d 180 -j -i $curLetter -y 0 -e $outfile
			"/c/Program Files (x86)/Inkscape/inkscape.com" -z -f "Svg/$f" -d 180 -j -i "0x$(printf "%02x" $i)" -y 0 -e "$PWD/${lang}ref/$curLetter.png"
		else
			echo "$outfile does not exist, continuing"
		fi
	done
	
	for i in {1..9}
	do
		curLetter="Letter_0x1$(printf "%02x" $i)"
		outfile="$PWD/$lang/$curLetter.png"
		if [ -z "$replacing" ] || [ -e $outfile ]
		then
			"/c/Program Files (x86)/Inkscape/inkscape.com" -z -f "Svg/$f" -d 180 -j -i $curLetter -y 0 -e $outfile
			"/c/Program Files (x86)/Inkscape/inkscape.com" -z -f "Svg/$f" -d 180 -j -i "0x1$(printf "%02x" $i)" -y 0 -e "$PWD/${lang}ref/$curLetter.png"
		else
			echo "$outfile does not exist, continuing"
		fi	
	done
	
	for finished in `ls $lang/`
	do
		echo "Resizing $finished"
		refDim=`identify "${lang}ref/$finished" | awk '{ print $3 }'`
		mogrify -background "#00000000" -gravity center -extent $refDim "$lang/$finished"
	done
done
