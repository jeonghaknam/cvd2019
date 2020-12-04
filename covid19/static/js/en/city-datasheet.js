var myChart = echarts.init(document.getElementById('datasheet2'), null, {devicePixelRatio: 2.5});
        var option = {
			    title: {
			        text: 'Total confirmed',
					x:'center',
        			y:'top',
			    },
			    tooltip: {
			        trigger: 'axis',
			        axisPointer: {
			            type: 'shadow'
			        }
			    },
			    legend: {
			    	x:'left',
			        data: ['Total confirmed']
			    },
			    grid: {
			        left: '1%',
			        right: '4%',
			        bottom: '3%',
			        containLabel: true
			    },
			    xAxis: {
			        type: 'log',
			        boundaryGap: [0, 0.01]
			    },
			    yAxis: {
			        type: 'category',
			        data: datasheet21,
			    },
			    series: [
			        {
			            name: 'Total confirmed',
			            type: 'bar',
			            data: datasheet22,
			        },
			    ]
			};

        myChart.setOption(option);