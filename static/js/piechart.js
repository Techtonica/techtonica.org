let ctx = document.getElementById("myChart").getContext("2d");
let labels = [
  "Black",
  "Latinx",
  "East Asian",
  "Southeast Asian",
  "White",
  "Central & South Asian",
  "Pacific Islander & Indigenous/First Nations & Middle Eastern"
];
let colorHex = [
  "rgb(75, 192, 192)",
  "rgb(54, 162, 235)",
  "rgb(201, 155, 203)",
  "rgb(255, 99, 132)",
  "rgb(255, 163, 140)",
  "rgb(255, 159, 64)",
  "rgb(255, 205, 86)"
];

let myChart = new Chart(ctx, {
  type: "pie",
  data: {
    labels: labels,
    datasets: [{
      label: "Techtonica Demographics",
      backgroundColor: colorHex,
      data: [22, 24, 19, 12, 14, 7, 2],
    }],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false, // Changed this line
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
  let width = Math.min(2880, window.innerWidth);
  let height = Math.min(1800, window.innerHeight);

  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';

  // Update chart size
  myChart.resize();
}

// Initial resize
resizeChart();

// Resize on window resize
window.addEventListener('resize', resizeChart);
