import gmplot 
  
# from_geocode method return the 
# latitude and longitude of given location . 
gmap2 = gmplot.GoogleMapPlotter.from_geocode('Hubei') 
  
gmap2.draw( "map2.html" ) 