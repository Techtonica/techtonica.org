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

    datasets: [
      {
        label: "Techtonica Demographics",
        backgroundColor: colorHex,
        data: [22, 24, 19, 12, 14, 7, 2],
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
    label: {
      display: true,
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
