var myChart = echarts.init(document.getElementById('transition'), null, {devicePixelRatio: 2.5});
        var option = {
               title: {
               	x:'center',
        text: 'Domestic Corona 19'
    },
    tooltip: {
        trigger:'axis',
    },
	color: ["#f15206de","#08fdf2","#ea0505",],
    legend: {
    	x:'center',
		y:'30px',
        data:this.legend,
        selected:{'Isolation':false, 'Recovered':true,'New Confirmed':true,}
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
            name: 'Isolation',
            type: 'line',
            data: transition2,
        },
		{
			name: 'Recovered',
			type: 'line',
			data: transition3,
		},
		{
			name: 'New Confirmed',
			type: 'line',
			data: transition4,
		},

    ]
            };
        myChart.setOption(option);