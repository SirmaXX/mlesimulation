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
    if (x > alpha) {
    return (beta / eta) * Math.pow((x - alpha) / eta, beta - 1) * Math.exp(-Math.pow((x - alpha) / eta, beta));
    }else{
        return 0;
    }
}

function sequencebuilder(start,end,step) {

    var start = 0.05;
    var end = 5;

    
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
    const std=Math.sqrt(sigmas);
    const high = mu + 3 * std;
   
    var xValues = sequencebuilder(alpha, high, 0.1);
   
    var yValues = xValues.map(function(x) {
        var pdfValue = weibullPDF(x, alpha, beta, eta).toFixed(2);
        console.log("x:", x, "PDF:", pdfValue);
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


/*      İnverse chisquare distribution     */


function mean_of_inversechi(v) {
    if (v > 2) {
    return 1/(v-2);
    }else{
     return 0;
    }

}




function variance_of_inversechi(v) {
    if (v > 2) {
    return 2/(Math.pow(v-2,2) * (v-4));
    }else{
     return 0;
    }

}



function inverseChiSquarePDF(x, v) {
    if (x <= 0 || v <= 0) {
        throw new Error("Both x and degrees of freedom (v) must be greater than 0");
    }

    const numerator = Math.pow(2, -v / 2);
    const denominator = jStat.gammafn(v / 2);
    const exponent = -1 / (2 * x);

    const pdfValue = (numerator / denominator) * Math.pow(x, -(v / 2) - 1) * Math.exp(exponent);

    return pdfValue;
}



function  inverseChiSquareGraph(canvasid, v) {

    const mu = mean_of_inversechi(v);
    const sigmas = variance_of_inversechi(v);
    const std=Math.sqrt(sigmas);
    const high = mu + 3 * std;
   
    var xValues = sequencebuilder(0, high, 0.1);
   
    var yValues = xValues.map(function(x) {
        var pdfValue =inverseChiSquarePDF(x, v).toFixed(2);
        console.log("x:", x, "PDF:", pdfValue);
        return inverseChiSquarePDF(x,v).toFixed(2);
    });

    // Create a line chart

    new Chart("" + canvasid + "",{
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                label: 'İnverse Chi Square PDF plot',
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

