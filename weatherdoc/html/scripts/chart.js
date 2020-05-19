    chartIt();



    async function getISS() {
        const api_url = 'https://k0wa1un85b.execute-api.us-east-1.amazonaws.com/production/books/';
        const response = await fetch(api_url);
        const data = await response.json();
        const xs = [];
        const ys = [];
        console.log(data);

        for (i = 0; i < data.body.length; i++){
        var CreateDataMin = data.body[i].CreateDataMin;
        var lowTemp = data.body[i].lowTemp;
        console.log(CreateDataMin);

        xs.push(CreateDataMin);
        ys.push(lowTemp);
        document.getElementById('CreateDataMin').textContent = CreateDataMin;
          }
          return { xs , ys };
    }


    async function chartIt(){
        const data = await getISS();
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.xs,
                datasets: [{
                    label: '# Temperature',
                    data:data.ys,
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }