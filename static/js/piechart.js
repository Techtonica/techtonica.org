/* what is the error?
1. ctx variable only should run when on the sponser page
2. it should not run anywhere else

pseudocode://this did not work
1. if current web page = sponsor
2. let ctx variable = document.getElementById("myChart").getContext
3. if not, set ctx variable to null
*/

//below also didn't work

// if(window.location.href === '127.0.0.1:5000/sponsor/') {
//   let ctx = document.getElementById("myChart").getContext("2d")
// } else {
//   let ctx = null
// }

//let ctx = document.getElementById("myChart").getContext("2d");

//solution: encase entire file in if statement:

let pieChart = document.getElementById("myChart");

if (pieChart) {
  let chartMod = pieChart.getContext("2d");

  let labels = [
    "Black",
    "Latinx",
    "East Asian",
    "Southeast Asian",
    "White",
    "Central & South Asian",
    "Pacific Islander & Indigenous/First Nations & Middle Eastern",
  ];
  let colorHex = [
    "rgb(75, 192, 192)",
    "rgb(54, 162, 235)",
    "rgb(201, 155, 203)",
    "rgb(255, 99, 132)",
    "rgb(255, 163, 140)",
    "rgb(255, 159, 64)",
    "rgb(255, 205, 86)",
  ];

  let myChart = new Chart(chartMod, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Techtonica Demographics",
          backgroundColor: colorHex,
          data: [22, 24, 19, 12, 14, 7, 2],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: 20,
      },
      legend: {
        display: true,
        position: "bottom",
        align: "center",
        labels: {
          fontColor: "#ffffff",
        },
      },
      plugins: {
        datalabels: {
          color: "#fff",
          anchor: "center",
          align: "center",
          offset: 0,
          borderWidth: 2,
          borderColor: "#fff",
          borderRadius: 25,
          clip: false,
          backgroundColor: (context) => {
            return context.dataset.backgroundColor;
          },
          font: {
            weight: "bold",
            size: 16, // Increased font size
          },
          formatter: (value, context) => {
            return value + "%";
          },
        },
      },
    },
  });

  // Function to resize the chart
  function resizeChart() {
    let canvas = document.getElementById("myChart");
    let width = Math.min(2880, window.innerWidth * 0.8);
    let height = Math.min(1800, window.innerHeight * 0.6);

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    // Update chart size
    myChart.resize();
  }

  // Initial resize
  resizeChart();

  // Resize on window resize
  window.addEventListener("resize", resizeChart);
}
