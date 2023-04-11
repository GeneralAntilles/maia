var chart = bb.generate({
    data: {
        url: "./scores/?format=json",
        mimeType: "json",
        keys: { x: "name", value: ["Score"] },
        type: "bar",
    },
    axis: {
        x: { type: "category" },
        y: { min: 0, max: max_score, padding: 0 }
    },
    legend: { show: false },
    bindto: "#result-bar-chart"
});