import gmplot

latitude_list = [30.975640000000002,40.18238,22.3193] # 22.3193,114.1694

longitude_list = [112.2707,116.4142,114.1694]

gmap = gmplot.GoogleMapPlotter(30.975640000000002,112.2707, 5 ) 

# heatmap plot heating Type
# points on the Google map
gmap.heatmap( latitude_list, longitude_list )

gmap.draw( "HeatMap.html" )