import gmplot 
  
# GoogleMapPlotter return Map object 
# Pass the center latitude and 
# center longitude 
gmap1 = gmplot.GoogleMapPlotter(30.975640000000002,112.2707, 13 ) 
  
# Pass the absolute path 
gmap1.draw( "map.html" ) 