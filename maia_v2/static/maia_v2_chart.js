// Histogram chart comparing against the overall total score distribution
// of all users
var histogram_chart = bb.generate({
    data: {
        url: "./stats/?format=json",
        mimeType: "json",
        keys: { x: "data1", value: ["Respondents"] },
        type: "bar",
    },
    axis: {
        y: { padding: 0 }
    },
    bar: { width: { ratio: 1 } },
    legend: { hide: true },
    color: function(color, d) {
        console.log(d);
        if (d.value == total_score) { return "#ff0000"; }
        return color;
    },
    bindto: "#result-hist-chart",
});

var bar_chart = bb.generate({
    data: {
        url: "./scores/?format=json",
        mimeType: "json",
        keys: { x: "name", value: ["Score"] },
        type: "bar",
    },
    axis: {
        x: {
            type: "category", tick: {
                format: function (index, categoryName) {
                    // Add a newline after a hyphen if there's no space
                    return categoryName.replace("-", "-\n");
                }
            }
        },
        y: { min: 0, max: max_score, padding: 0 }
    },
    legend: { position: "bottom" },
    bindto: "#result-bar-chart",
    oninit: function() {
        this.load({
            url: "./comparison/?format=json",
            mimeType: "json",
            keys: { x: "name", value: ["Museum visitors", "Hospital pre-treatment", "Hospital post-treatment"] },
            type: "bar",
        });
    }
});
