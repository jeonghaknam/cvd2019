var myChart = echarts.init(document.getElementById('worldtransition'), null, {devicePixelRatio: 2.5});
        var option = {
               title: {
               	x:'center',
        text: 'World COVID19'
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
        data: worldtransition1,
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'Isolation',
            type: 'line',
            data: worldtransition2,
        },
		{
			name: 'Recovered',
			type: 'line',
			data: worldtransition3,
		},
		{
			name: 'New Confirmed',
			type: 'line',
			data: worldtransition4,
		},

    ]
            };
        myChart.setOption(option);