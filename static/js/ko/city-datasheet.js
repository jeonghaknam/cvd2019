var myChart = echarts.init(document.getElementById('datasheet2'), null, {devicePixelRatio: 2.5});
        var option = {
			    title: {
			        text: '도시별 총확진자',
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
			        data: ['총확진']
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
			            name: '총확진',
			            type: 'bar',
			            data: datasheet22,
			        },
			    ]
			};

        myChart.setOption(option);