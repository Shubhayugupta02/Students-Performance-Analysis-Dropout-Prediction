google.charts.load("current", {packages:["corechart"]});

async function loadDashboard(){
  const res = await fetch("/api/dashboard-data");
  const data = await res.json();

  drawRiskPie(data);
  drawAttendanceLine(data);
  drawScoreBar(data);
}

function drawRiskPie(d){
  const table = google.visualization.arrayToDataTable([
    ["Risk","Count"],
    ["Low",d.low],
    ["Medium",d.medium],
    ["High",d.high]
  ]);

  new google.visualization.PieChart(
    document.getElementById("riskPie")
  ).draw(table,{
    backgroundColor:"transparent",
    pieHole:0.5,
    colors:["#00ffcc","#ffaa00","#ff2f6d"]
  });
}

function drawAttendanceLine(d){
  const rows=[["Attempt","Attendance"]];
  d.attendance.forEach((v,i)=>rows.push([`${i+1}`,v]));

  new google.visualization.LineChart(
    document.getElementById("attendanceLine")
  ).draw(google.visualization.arrayToDataTable(rows),{
    backgroundColor:"transparent",
    colors:["#00f6ff"]
  });
}

function drawScoreBar(d){
  const rows=[["Attempt","Score"]];
  d.scores.forEach((v,i)=>rows.push([`${i+1}`,v]));

  new google.visualization.ColumnChart(
    document.getElementById("scoreBar")
  ).draw(google.visualization.arrayToDataTable(rows),{
    backgroundColor:"transparent",
    colors:["#ff2fd6"]
  });
}

loadDashboard();
