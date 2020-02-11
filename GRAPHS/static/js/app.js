// creating colored world map

var mapConfig = {
  center: [10, 0],
  zoom: 2
}

var tileURL = "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}"

var tileConfig = {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.streets",
accessToken: "pk.eyJ1IjoiamJlcnNpbmljIiwiYSI6ImNrNXgzdm56ejAxd3kzbWw1ZWdrMTRkOWgifQ.WNwFvtjg1IHKQ-RULtIJkg"
}

var geoJSONurl = 'static/data/countries.geo.json'

function colorChooser(name) {
  if (10 <= 10) {
      return "blue"
  }
  else {
      return "green"
  }
};

function worldmap(){

  var map = L.map("map", mapConfig)
  var mapLayer = L.tileLayer(tileURL, tileConfig).addTo(map)
  d3.json(geoJSONurl, function(data) {
    L.geoJSON(data, {
        style: function(feature) {
            return {
                color: "white",
                fillColor: colorChooser(feature.properties.name),
                fillOpacity: 0.5,
                weight: 1.5
              };
        }, 
        onEachFeature : function (feature, layer) {
                layer.on({
                    mouseover: function(event) {
                        layer = event.target, 
                        layer.setStyle({
                            fillOpacity: 0.75
                        });
                    }, 
                    mouseout: function(event) {
                        layer = event.target, 
                        layer.setStyle({
                            fillOpacity: 0.5
                        })
                    }
                });
                layer.bindPopup("<h1>" + feature.properties.name + "</h1><hr><h2>" + feature.properties.id + "</h2>");
        }
    }).addTo(map);
  });

}
worldmap();

// creating world emissions line chart

function worldemissions(country,field){

  trace1 ={
    x:country.year,
    y:country.value,
    mode:"scatter",
    
  } 
  ldata1=[trace1];
  layout1 = {
      title: `${country} ${field} v/s Time`,
      showlegend: true,
      height: 600,
      width: 1200,
      xaxis: { 
          title:"Year"
      },
      yaxis: { 
        title:`${field} (Megatonnes)`
    },
    }
  Plotly.newPlot("scatter",ldata1,layout1)

}

//worldemissions(world);

// grabbing the country and field

var country = d3.selectAll("#country").property("value")
var field = d3.selectAll("#field").property("value")

//creating country specific line chart
//worldemissions(country,field);




