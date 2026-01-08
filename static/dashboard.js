google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(loadDashboard);

function loadDashboard() {
  fetch("/api/dashboard-data")
    .then(r => r.json())
    .then(d => {

      const pie = google.visualization.arrayToDataTable([
        ["Risk", "Count"],
        ["Low", d.low],
        ["Medium", d.medium],
        ["High", d.high]
      ]);

      new google.visualization.PieChart(
        document.getElementById("riskPie")
      ).draw(pie, {
        pieHole: 0.45,
        backgroundColor: "transparent",
        colors: ["#00ffcc", "#ffaa00", "#ff2fd6"]
      });

      const att = [["Index", "Attendance"]];
      d.attendance.forEach((v, i) => att.push([i + 1, v]));

      new google.visualization.LineChart(
        document.getElementById("attendanceLine")
      ).draw(
        google.visualization.arrayToDataTable(att),
        { backgroundColor: "transparent", colors: ["#00f6ff"] }
      );

      const score = [["Index", "Score"]];
      d.scores.forEach((v, i) => score.push([i + 1, v]));

      new google.visualization.LineChart(
        document.getElementById("scoreLine")
      ).draw(
        google.visualization.arrayToDataTable(score),
        { backgroundColor: "transparent", colors: ["#ff2fd6"] }
      );
    });
}
