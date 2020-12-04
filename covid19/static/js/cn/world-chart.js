var myChart = echarts.init(document.getElementById('worldtransition'), null, {devicePixelRatio: 2.5});
        var option = {
               title: {
               	x:'center',
        text: '世界新型肺炎疫情趋势'
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

        data: worldtransition1,
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '现有确诊',
            type: 'line',
            data: worldtransition2,
        },
		{
			name: '治愈',
			type: 'line',
			data: worldtransition3,
		},
		{
			name: '新增确诊',
			type: 'line',
			data: worldtransition4,
		},

    ]
            };
        myChart.setOption(option);