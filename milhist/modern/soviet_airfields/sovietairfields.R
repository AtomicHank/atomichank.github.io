library(raster)
library(leaflet)
library(measurements)
library(ggmap)
library(ggplot2)
library(htmltools)
#Loads Libraries

airinfrastr <- read.csv("sovietbases.csv", stringsAsFactors = FALSE)
#Reads .csv files and brings them in as data frames

leaflet() %>%
  #Creates a map widget
  
  setView(lng = 16.5, lat = 48.7, zoom = 4) #%>%
  #Centers the map on a long and lat (AUS/CZ Border) and sets the zoom at 5; lower the number to zoom out
  
  #addProviderTiles("Esri.WorldImagery", group="Imagery (default)") %>% #background imagery
  addProviderTiles("Esri.NatGeoWorldMap", group="Imagery (default)") %>% #background imagery
  #Sets the type of map leaflet will use; list of map types found at leaflet-extras.github.io/leaflet-providers/preview/
  
  addCircleMarkers(data = airinfrastr, 
                   #Add points to the base map
                   #Places markers associated with location
                   lat = ~latitude, 
                   #Imports the lat associated with locations 
                   lng = ~longitude, 
                   #Imports the long associated with locations 
                   radius = 4,
                   color = "orange",
                   #Sets the radius of the markers at 4 and the color to orange
                   stroke = FALSE, fillOpacity = 1,
                   group = "Air Infrastructure",
                   popup = paste("<b><u>NAME:</u></b>", airinfrastr$name, "<br>",
                                 "<b><u>ICAO:</u></b>", airinfrastr$iaco, "<br>",
                                 "<b><u>Use:</u></b>", airinfrastr$use, "<br>",
                                 #"<b><u>Role:</u></b>", airinfrastr$role, "<br>",
                                 "<b><u>Notes:</u></b>", airinfrastr$notes))%>%
  
  addLayersControl(
    overlayGroups = c("Air Infrastructure"),
    options = layersControlOptions(collapsed = FALSE) 
  ) %>%
  
  hideGroup("Air Infrastructure")


