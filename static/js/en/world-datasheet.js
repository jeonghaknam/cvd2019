var myChart = echarts.init(document.getElementById('datasheet'), null, {devicePixelRatio: 2.5});
        var option = {
			    title: {
			        text: 'Total confirmers',
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
			        data: datasheet11,
			    },
			    series: [
			        {
			            name: 'Total confirmed',
			            type: 'bar',
			            data: datasheet12,
			        },
			    ]
			};

        myChart.setOption(option);