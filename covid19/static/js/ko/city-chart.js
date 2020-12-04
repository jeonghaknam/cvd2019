var myChart = echarts.init(document.getElementById('transition'), null, {devicePixelRatio: 2.5});
        var option = {
               title: {
               	x:'center',
        text: '국내 코로나19 추세'
    },
    tooltip: {
        trigger:'axis',
    },
	color: ["#f15206de","#08fdf2","#ea0505",],
    legend: {
    	x:'center',
		y:'30px',
        data:this.legend,
        selected:{'격리/치료중':false, '격리해제/완치':true,'신규확진':true,}
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
            name: '격리/치료중',
            type: 'line',
            data: transition2,
        },
		{
			name: '격리해제/완치',
			type: 'line',
			data: transition3,
		},
		{
			name: '신규확진',
			type: 'line',
			data: transition4,
		},

    ]
            };
        myChart.setOption(option);