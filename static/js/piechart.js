let ctx = document.getElementById("myChart").getContext("2d");
let labels = ["Black", "East Asian", "White", "South East Asian", "Latinx"];
let colorHex = [
  "rgb(255, 99, 132)",
  "rgb(255, 159, 64)",
  "rgb(255, 205, 86)",
  "rgb(75, 192, 192)",
  "rgb(54, 162, 235)",
];

let myChart = new Chart(ctx, {
  type: "pie",
  data: {
    labels: labels,

    datasets: [
      {
        label: "Techtonica Demographics",
        backgroundColor: colorHex,
        data: [32, 14, 9, 9, 36],
      },
    ],
  },

  options: {
    responsive: false,
    legend: {
      display: true,
      position: "bottom",
      labels: {
        fontColor: "#ffffff",
      },
    },
    labels: {
      display: false,
    },

    plugins: {
      datalabels: {
        color: "#fff",
        anchor: "end",
        align: "start",
        offset: -3,
        borderWidth: 2,
        borderColor: "#fff",
        borderRadius: 25,
        clip: "false",
        backgroundColor: (context) => {
          return context.dataset.backgroundColor;
        },
        font: {
          weight: "bold",
          size: 10,
        },
        formatter: (value, context) => {
          return value + "%";
        },
      },
    },
  },
});
