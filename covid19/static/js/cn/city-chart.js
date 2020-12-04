var myChart = echarts.init(document.getElementById('transition'), null, {devicePixelRatio: 2.5});
        var option = {
               title: {
               	x:'center',
        text: '韩国新型肺炎疫情趋势'
    },
    tooltip: {
        trigger:'axis',
    },
	color: ["#f15206de","#08fdf2","#ea0505",],
    legend: {
    	x:'center',
		y:'30px',
        data:this.legend,
        selected:{'现有确诊':false, '治愈':true,'新增确诊':true,}
    },
    grid: {
        left: 'auto',
        right: '4%',
        bottom: '5%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
		axisLabel : {
            formatter: function(value){
                return value.slice(5,).replace('월','.').replace('일','');}
            },

        data: transition1,
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '现有确诊',
            type: 'line',
            data: transition2,
        },
		{
			name: '治愈',
			type: 'line',
			data: transition3,
		},
		{
			name: '新增确诊',
			type: 'line',
			data: transition4,
		},

    ]
            };
        myChart.setOption(option);