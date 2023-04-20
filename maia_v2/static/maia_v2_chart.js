// Dark mode and light mode color defaults
if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    Chart.defaults.backgroundColor = 'hsl(51, 14%, 90%)';
    Chart.defaults.borderColor = '#56545a';
    Chart.defaults.color = '#e9e8e2';
}
var colors = [
    '#f51911a8',
    '#955196a8',
    '#ff6e54a8',
    '#dd5182a8',
    '#ffa600a8',
    '#bf8ddba8',
    '#5ac5d8a8',
];

let barChart;
let histogramChart;

// Histogram chart comparing against the overall total score distribution
// of all users
async function fetchStats(url) {
    const response = await fetch(url)
    const jsonData = await response.json();

    const labels = jsonData.data1
    const values = jsonData.Respondents

    return [labels, values];
}

function getBackgroundColor(labels, bucket) {
    return labels.map(label => (label === bucket ? '#f51911' : 'rgba(75, 192, 192, 0.85)'));
}

async function generateHistogramChart() {
    const [labels, values] = await fetchStats('./stats/?format=json');

    const histogram = document.getElementById('result-hist-chart');
    histogramChart = new Chart(histogram, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Respondents',
                data: values,
                backgroundColor: getBackgroundColor(labels, bucket),
                barPercentage: 1.26,
            }],
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true },
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: (items) => {
                            if (!items.length) {
                                return '';
                            }
                            const item = items[0];
                            const x = parseFloat(item.label);
                            const min = (x - (5 / labels.length)).toPrecision(2);
                            const max = (x + (5 / labels.length)).toPrecision(2);
                            return `${min} - ${max}`;
                        },
                    }
                },
            },
        },
    });
}

async function fetchData(url) {
    const response = await fetch(url)
    const jsonData = await response.json();

    const labels = jsonData.map(item => item.name);
    const values = jsonData.map(item => item.value);

    return [labels, values];
}

async function generateDataDictionary(you, comparison_url) {
    const response = await fetch(comparison_url)
    const comparison = await response.json();
    datasets = [{
        label: 'You',
        data: you,
        backgroundColor: colors[colors.length - 1],
    }];
    const keys = Object.keys(comparison);
    for (let i = 0; i < keys.length; i++) {
        const name = keys[i];
        const values = comparison[name].map(item => item.value);

        datasets.push({
            label: name,
            data: values,
            backgroundColor: colors[i],
        });
    }

    return datasets;
}

async function fetchDataCreateChart() {
    const bar_score_url = './scores/?format=json';
    const bar_comparison_url = './comparison/?format=json';

    try {
        const [labels, values] = await fetchData(bar_score_url);
        const comparison = await generateDataDictionary(values, bar_comparison_url);

        // Create a new instance of Chart.js bar chart with the fetched data
        const ctx = document.getElementById('result-bar-chart').getContext('2d');
        barChart = new Chart(ctx, {
            type: 'bar',
            data: { labels: labels, datasets: comparison },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                },
                indexAxis: (window.innerWidth < 768) ? 'y' : 'x',
                interaction: { intersect: false, mode: 'index' },
                aspectRatio: 1,
                onResize: function (chart, size) {
                    if (size.width < 715) {
                        chart.options.indexAxis = 'y';
                    } else {
                        chart.options.indexAxis = 'x';
                    }
                },
                resizeDelay: 100,
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


generateHistogramChart();
fetchDataCreateChart();
