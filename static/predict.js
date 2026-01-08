google.charts.load("current", { packages: ["corechart", "gauge"] });

function analyzeRisk() {

  const payload = {
    model: document.getElementById("model").value,
    attendance: document.getElementById("attendance").value,
    marks: document.getElementById("marks").value,
    study_hours: document.getElementById("study_hours").value,
    failures: document.getElementById("failures").value
  };

  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(d => {

    document.getElementById("result-box").innerHTML = `
      <h3>Risk Level: ${d.risk}</h3>
      <p>Score: ${d.score}</p>
      <p>Confidence: ${d.confidence}%</p>
    `;

    document.getElementById("alertBox").innerHTML =
      d.alert ? `<div class="alert">HIGH RISK – Immediate Intervention Needed</div>` : "";

    drawGauge(d.confidence);
    drawImportance(d.importance);
  });
}

function drawGauge(value) {

  const data = google.visualization.arrayToDataTable([
    ["Label", "Value"],
    ["Confidence", value]
  ]);

  const options = {
    min: 0,
    max: 100,
    greenFrom: 70,
    greenTo: 100,
    yellowFrom: 40,
    yellowTo: 70,
    redFrom: 0,
    redTo: 40
  };

  new google.visualization.Gauge(
    document.getElementById("confidenceGauge")
  ).draw(data, options);
}

function drawImportance(imp) {

  const rows = [["Feature", "Weight"]];
  Object.keys(imp).forEach(k => rows.push([k, imp[k]]));

  const data = google.visualization.arrayToDataTable(rows);

  new google.visualization.BarChart(
    document.getElementById("importanceBar")
  ).draw(data, {
    backgroundColor: "transparent",
    legend: { position: "none" },
    colors: ["#ff2fd6"]
  });
}
