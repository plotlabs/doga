import { Doughnut } from "react-chartjs-2";
export default function DoughnutChart({ data }) {
  let labels = [];
  let dataset = [];
  let totalFields = 0;
  for (let key in data?.tables) {
    labels.push(data?.tables[key].table_name);
    dataset.push(data?.tables[key].no_fields);
    totalFields += data?.tables[key].no_fields;
  }

  const dataDoughnut = {
    labels: ["Tables", "Relations", "Fields", "Exported"],

    datasets: [
      {
        data: [
          data?.number_of_tables,
          data?.relationships?.length || 0,
          totalFields,
          data?.deployment_info?.total_no_exports,
        ],
        backgroundColor: ["#7cb9e873", "#1D487B", "#6e798c9c"],
        hoverBackgroundColor: ["#7cb9e873", "#1D487B", "#6e798c9c"],
      },
    ],
    text: "23%",
  };

  return (
    <Doughnut
      data={dataDoughnut}
      height={"100%"}
      width={"100%"}
      options={{
        maintainAspectRatio: false,
        legend: {
          position: "right",
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: true,
                zeroLineColor: "gray",
              },

              ticks: {
                display: false,
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: true,
              },
              ticks: {
                display: false,
                beginAtZero: true,
              },
            },
          ],
        },
      }}
    />
  );
}
