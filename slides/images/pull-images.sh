#!/bin/bash

this_dir="`dirname $0`"

if [ "$this_dir" = '.' ]
then
    base_dir="`pwd`"
else
    cd "$this_dir"
    base_dir="`pwd`"
fi

curl -o darwin-tol-copyright-boris-kulikov-2007.jpg http://www.boriskulikov.com/images/DarwinTreeOfLife-%20L.jpg
curl -o kane.jpg http://uwberg.com/wp-content/uploads/2014/05/berg-hero.jpg
curl -o mascot-tulane-green-wave.png http://upload.wikimedia.org/wikipedia/en/9/9e/TulaneGreenWave.png
curl -o mascot-sewanee-tiger.jpg http://www.sewaneetigers.com/sports/wbkb/2010-11/releases/MBB%200115110836.html%20h35g7.jpeg
curl -o mascot-georgia-tech-yellow-jacket.png http://upload.wikimedia.org/wikipedia/en/8/8f/GeorgiaTechYellowJackets.png
curl -o mascot-alabama-big-al.gif http://www.survivingcollege.com/wp-content/uploads/2013/07/University-of-Alabama-Crimson-Tide-Big-Al-Elephant-Mascot-Logo.gif
convert mascot-alabama-big-al.gif mascot-alabama-big-al.png
curl -o mascot-florida-gator.png http://upload.wikimedia.org/wikipedia/en/thumb/1/12/Florida_Gators_logo.svg/470px-Florida_Gators_logo.svg.png
curl -o mascot-sc-gamecock.png http://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/South_Carolina_Gamecocks_Block_C_logo.svg/182px-South_Carolina_Gamecocks_Block_C_logo.svg.png
curl -o mascot-vanderbilt-commodore.png http://redanglespanish.files.wordpress.com/2011/12/commodore.png
curl -o mascot-vanderbilt-commodore-cartoon.gif http://www.nashvillescene.com/binary/0511/vanderbilt_mascot.gif
convert mascot-vanderbilt-commodore-cartoon.gif mascot-vanderbilt-commodore-cartoon.png
curl -o mascot-texas-am-reveille.gif http://content.sportslogos.net/logos/34/866/thumbs/86645362001.gif
convert mascot-texas-am-reveille.gif mascot-texas-am-reveille.png
curl -o mascot-tennessee-smokey.png http://content.sportslogos.net/logos/34/861/full/2892_tennessee_volunteers-mascot-2005.png
curl -o mascot-arkansas-razorback.png http://upload.wikimedia.org/wikipedia/commons/e/ef/Arkansas-Razorback-Logo-2001.png
curl -o mascot-ole-miss-rebel-black-bear.jpg http://uwire.com/wp-content/uploads/2010/10/news_bear_contrib.jpg
curl -o mascot-georgia-bulldog.jpg http://www.saturdaydownsouth.com/wp-content/uploads/2013/04/new-uga-logo.jpg
curl -o mascot-mississippi-state-bulldog.gif http://content.sportslogos.net/logos/32/755/full/hyoflhueqc3u3whapwey2gjnj.gif
convert mascot-mississippi-state-bulldog.gif mascot-mississippi-state-bulldog.png
curl -o mascot-kentucky-wild-cat.jpg https://www.louisville.com/sites/default/files/u1321/Kentucky_Wildcats.jpg
curl -o mascot-lsu-tiger.jpg http://nashvillesportsmix.com/wp-content/uploads/2014/06/LSU1.jpg
curl -o mascot-auburn-eagle-tiger.jpg http://cdn2.sbnation.com/assets/3402903/auburn_eagle_tigers_copy.jpg
curl -o mascot-auburn-war-eagle.jpg https://thewareaglereader.files.wordpress.com/2008/07/image001.jpg
curl -o mascot-auburn-war-eagle-cartoon.jpg https://lh3.ggpht.com/CQNJ446dAfFUfGL8A2FZs-0Ul0ZCpOYqZRhWoWiUTXoOrLqdVFNFbs1MmyUmeTRQlr0=h900
curl -o mascot-auburn-tiger.png http://content.sportslogos.net/logos/30/610/full/8809_auburn_tigers-primary-1957.png
curl -o mascot-missouri-tiger.png http://upload.wikimedia.org/wikipedia/en/5/50/MizzouPrimaryAthleticMark.png
