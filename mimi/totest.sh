# call e.g. as: sh totest.sh Psalms_027
D=/Users/Christiaan/Sites/brat/data/mimi-test/annotate

chgrp _www "$1.ann" "$1.txt"
chmod 664 "$1.ann"
cp -p "$1.ann" "$1.txt" $D
