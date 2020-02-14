// grabbing the country and field
d3.select("#countrybutton").on("click",grabber)
function grabber(){
  var countryInput = d3.selectAll("#country").property("value")
  var fieldInput  = d3.selectAll("#field").property("value")
  var urlcountry = "/api/emission/" + countryInput +"/" + fieldInput
  console.log(urlcountry)
  d3.json(urlcountry).then(function(response) {
    worldemissions(response)
  })
}

function worldemissions(emission){
  a=emission.filter(d=>d[0].variable=="historic")
  console.log(a)
  // if (emission[0].variable =="historic" ){
  //   console.log("yoooo")
  //   trace1 ={
  //     x:emission[0].year,
  //     y:emission[0].value,
  //     text:emission[0].value ,
  //     mode:"scatter",
  //   } 
  // }
  // else if(emission[0].variable =="projected_current_policy_min" ){
  //   console.log("yoooo2")
  //   trace2 ={
  //     x:emission[0].year,
  //     y:emission[0].value,
  //     text:emission[0].value ,
  //     mode:"scatter",
  //   }
  // }
  // else{
  //   console.log("yooooelse")
  // }

  // ldata1=[trace1,trace2];
  // layout1 = {
  //     title: `${emission[0].country[0]} ${emission[0].indicator[0]} v/s Time`,
  //     showlegend: true,
  //     height: 600,
  //     width: 1200,
  //     xaxis: { 
  //         title:"Year"
  //     },
  //     yaxis: { 
  //       title:`${emission[0].indicator[0]} in ${emission[0].unit[0]} `
  //   },
  //   }
  // Plotly.newPlot("scatter",ldata1,layout1)

}