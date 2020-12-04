var myChart = echarts.init(document.getElementById('datasheet2'), null, {devicePixelRatio: 2.5});
        var option = {
			    title: {
			        text: '地区 总确诊',
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
			        data: ['总确诊']
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
			            name: '总确诊',
			            type: 'bar',
			            data: datasheet22,
			        },
			    ]
			};

        myChart.setOption(option);