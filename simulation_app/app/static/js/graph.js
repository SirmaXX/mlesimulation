function colorgenerator(n) {
    var colors = [];
    for (let i = 0; i < n; i++) {
      var randomColor = "#" + Math.floor(Math.random() * 16777215).toString(16);
      colors.push(randomColor);
    }
    return colors;
  }
  
  function dataseperator(arr, alpha) {
  
    value = (arr.length) * alpha;
    return Math.round(value);
  }
  
  
  function freq(arr) {
    newcount = []
    const counts = {};
    /*https://stackoverflow.com/questions/5667888/counting-the-occurrences-frequency-of-array-elements */
    for (const num of arr) {
      counts[num] = counts[num] ? counts[num] + 1 : 1;
      newcount.push(counts[num]);
    }
    return newcount;
  }
  


  function colorgenerator(n) {
    var colors = [];
    for (let i = 0; i < n; i++) {
      var randomColor = "#" + Math.floor(Math.random() * 16777215).toString(16);
      colors.push(randomColor);
    }
    return colors;
  }
  


  function mean_of_threeweibull(alpha, beta, eta) {
    const result = eta * jStat.gammafn(1 + (1 / beta)) + alpha;
    return result;
}

function variance_of_threeweibull(alpha, beta, eta) {
    const result = Math.pow(eta, 2) * (jStat.gammafn(1 + (2 / beta)) - Math.pow(jStat.gammafn(1 + (1 / beta)), 2));
    return result;
}

function inverse_of_threeweibull(p, alpha, beta, eta) {
    const quantile_value = alpha + eta * Math.pow(-Math.log(1 - p), 1 / beta);
    return quantile_value;
}

function datagenerator(n, alpha, beta, eta) {
    const generated_data = jStat.uniform.sample(n, 0, 1);
    const dataset = generated_data.map(i => inverse_of_threeweibull(i, alpha, beta, eta));
    return dataset;
}


function weibullPDF(x, alpha, beta, eta) {
    return (beta / eta) * Math.pow((x - alpha) / eta, beta - 1) * Math.exp(-Math.pow((x - alpha) / eta, beta));
}

function sequencebuilder(start,end,step) {

    var start = 0.05;
    var end = 5;
    var step = 0.001;
    
    // Create an array of values
    var x = [];
    for (var i = start; i <= end; i += step) {
        value = i.toFixed(2);
        x.push( value );
    }

    return x;
}

function WeibullGraph(canvasid, alpha, beta, eta) {

    const mu = mean_of_threeweibull(alpha, beta, eta);
    const sigmas = variance_of_threeweibull(alpha, beta, eta);

    var xValues = sequencebuilder(0.5, 1, 0.1);
   
    var yValues = xValues.map(function(x) {
        return weibullPDF(x, alpha, beta, eta).toFixed(2);
    });

    // Create a line chart

    new Chart("" + canvasid + "",{
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                label: 'Three-Parameter Weibull PDF',
                data: yValues,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                },
                y: {
                    type: 'linear',
                    position: 'left'
                }
            }
        }
    });
}