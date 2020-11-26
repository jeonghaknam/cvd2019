var myChart = echarts.init(document.getElementById('province'), null, {devicePixelRatio: 2.5});
        var option = {
                title : {
                },
                tooltip : {
                    trigger: 'item',
                    formatter:function(params){
                        var res=params.name+'<br />';
                        var myseries=option.series;
                        for(var i=0;i<myseries.length;i++){
                            for(var k=0;k<myseries[i].data.length;k++){
                                if(myseries[i].data[k].name==params.name){
                                    res+=myseries[i].name+'&nbsp;:&nbsp;'+myseries[i].data[k].value+'<br />';
                                }
                            }
                        }
                        return res;
                    }
                },
                legend: {
                    show: false,
                    orient: 'vertical',
                    x:'left',
                    data:this.legend,
                    selectedMode: false,
                    selected:{'격리중':true, '총확진':false, '사망자':false,}
                },
                dataRange: {
                    show:false,
                    x: 'left',
                    y: 'bottom',
                    splitList: [
                        {start: 100000,},
                        {start: 10001,end: 100000},
                        {start: 1001,end: 10000},
                        {start: 501,end: 1000},
                        {start: 101,end: 500},
                        {start: 1,end: 100},
                    ],
                    color: ['#9a1f35', '#fe4365', '#fc9d9a', '#f9cda9', '#c8c8a9', '#83af9b']
                },

                roamController: {
                    show: false,
                    x: 'left',
                    mapTypeControl: {
                        'china': false
                    }
                },
                series : [
                    {
                        name: '격리중',
                        type: 'map',
                        mapType: 'korea',
                        // 控制地图大小
                        mapLocation: {
                            x: '240',
                            y: 'center',
                            height: '75%'
                        },
                        showLegendSymbol: false,
                        roam: 'false',
                        itemStyle:{
                            normal:{
                                label:{
                                    show:false,
                                    textStyle: {
                                       color: "rgb(249, 249, 249)"
                                    }
                                }
                            },
                            emphasis:{label:{show:false}}
                        },
                        data: province11,
                        nameMap:{
                        	'부산': '부산',
							'충북': '충북',
							'충남': '충남',
							'대구': '대구',
							'대전': '대전',
							'강원': '강원',
							'광주': '광주',
							'경기': '경기',
							'경북': '경북',
							'경남': '경남',
							'인천': '인천',
							'제주도': '제주',
							'전북': '전북',
							'전남': '전남',
							'세종': '세종',
							'서울': '서울',
							'울산': '울산',
                        },
                    },
                    {
                        name: '총확진',
                        type: 'map',
                        showLegendSymbol: false,
                        itemStyle:{
                            normal:{
                                label:{show:false,}},
                            emphasis:{label:{show:false}}
                    	},
                        data: province22,
                    },
                    {
                        name: '사망자',
                        type: 'map',
                        showLegendSymbol: false,
                        itemStyle:{
                            normal:{
                                label:{show:false,}},
                            emphasis:{label:{show:false}}
                    },
                        data: province33,
                    }
                ]
            };
        myChart.setOption(option);