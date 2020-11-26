var myChart = echarts.init(document.getElementById('worldmap'), null, {devicePixelRatio: 2.5});
        var option = {
                title : {
                    // text: '',
                    // subtext: '',
                    // x:''
                },
                tooltip : {
                    trigger: 'item',
                },
                legend: {
                    show: false,
                    orient: 'vertical',
                    x:'left',
                    data:this.legend,
                    selectedMode: false,
                    selected:{'격리중':true,}
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
                    show: true,
                    x: 'left',
                    mapTypeControl: {
                        'world': true,
                    }
                },
                series : [
                    {
                        name: '격리중',
                        type: 'map',
                        mapType: 'world',
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
                        data: worldmap11,
                        nameMap:{
                            'USA': '미국',
							'Brazil': '브라질',
							'India': '인도',
							'Russia': '러시아',
							'Peru': '페루',
							'Chile': '칠레',
							'Mexico': '멕시코',
							'South Africa': '남아프리카공화국',
							'Spain': '스페인',
							'UK': '영국',
							'Iran': '이란',
							'Pakistan': '파키스탄',
							'Italy': '이탈리아',
							'Saudi Arabia': '사우디아라비아',
							'Turkey': '터키',
							'Germany': '독일',
							'Bangladesh': '방글라데시',
							'France': '프랑스',
							'Colombia': '콜롬비아',
							'Argentina': '아르헨티나',
							'Canada': '캐나다',
							'Qatar': '카타르',
							'Egypt': '이집트',
							'Iraq': '이라크',
							'China': '중국',
							'Indonesia': '인도네시아',
							'Sweden': '스웨덴',
							'Ecuador': '에콰도르',
							'Belarus': '벨라루스',
							'Kazakhstan': '카자흐스탄',
							'Belgium': '벨기에',
							'Oman': '오만',
							'Philippines': '필리핀',
							'Kuwait': '쿠웨이트',
							'Ukraine': '우크라이나',
							'UAE': '아랍에미리트',
							'Bolivia': '볼리비아',
							'Netherlands': '네덜란드',
							'Panama': '파나마',
							'Dominican Republic': '도미니카공화국',
							'Portugal': '포르투갈',
							'Singapore': '싱가포르',
							'Israel': '이스라엘',
							'Poland': '폴란드',
							'Afghanistan': '아프가니스탄',
							'Bahrain': '바레인',
							'Nigeria': '나이지리아',
							'Romania': '루마니아',
							'Armenia': '아르메니아',
							'Switzerland': '스위스',
							'Guatemala': '과테말라',
							'Honduras': '온두라스',
							'Ireland': '아일랜드',
							'Azerbaijan': '아제르바이잔',
							'Ghana': '가나',
							'Japan': '일본.',
							'Algeria': '알제리',
							'Moldova': '몰도바',
							'Serbia': '세르비아',
							'Austria': '오스트리아',
							'Nepal': '네팔',
							'Morocco': '모로코',
							'Cameroon': '카메룬',
							'Uzbekistan': '우즈베키스탄',
							'S. Korea': '한국',
							'Czechia': '체코',
							'Ivory Coast': '코트디부아르',
							'Denmark': '덴마크',
							'Kyrgyzstan': '키르기스스탄',
							'Kenya': '케냐',
							'El Salvador': '엘살바도르',
							'Australia': '호주',
							'Sudan': '수단',
							'Venezuela': '베네수엘라',
							'Norway': '노르웨이',
							'Costa Rica': '코스타리카',
							'Malaysia': '말레이시아',
							'North Macedonia': '북마케도니아',
							'Senegal': '세네갈',
							'Ethiopia': '에티오피아',
							'DRC': '콩고민주공화국',
							'Bulgaria': '불가리아',
							'Bosnia and Herzegovina': '보스니아 헤르체고비나',
							'Finland': '핀란드',
							'Palestine': '팔레스타인',
							'Haiti': '아이티',
							'Tajikistan': '타지키스탄',
							'French Guiana': '프랑스령 기아나',
							'Guinea': '기니',
							'Gabon': '가봉',
							'Madagascar': '마다가스카르',
							'Mauritania': '모리타니',
							'Luxembourg': '룩셈부르크',
							'Djibouti': '지부티',
							'CAR': '중앙아프리카공화국',
							'Hungary': '헝가리',
							'Croatia': '크로아티아',
							'Greece': '그리스',
							'Albania': '알바니아',
							'Thailand': '타이',
							'Paraguay': '파라과이',
							'Nicaragua': '니카라과',
							'Somalia': '소말리아',
							'Equatorial Guinea': '적도기니',
							'Maldives': '몰디브',
							'Mayotte': '마요트섬',
							'Sri Lanka': '스리랑카',
							'Malawi': '말라위',
							'Lebanon': '레바논',
							'Cuba': '쿠바',
							'Mali': '말리',
							'Congo': '콩고',
							'South Sudan': '남수단',
							'Estonia': '에스토니아',
							'Slovakia': '슬로바키아',
							'Iceland': '아이슬란드',
							'Zambia': '잠비아',
							'Lithuania': '리투아니아',
							'Slovenia': '슬로베니아',
							'Guinea-Bissau': '기니비사우',
							'Cabo Verde': '카보베르데',
							'Sierra Leone': '시에라리온',
							'Libya': '리비아',
							'Hong Kong': '홍콩',
							'New Zealand': '뉴질랜드',
							'Yemen': '예멘',
							'Eswatini': '에스와티니',
							'Rwanda': '르완다',
							'Benin': '베냉',
							'Mozambique': '모잠비크',
							'Tunisia': '튀니지',
							'Montenegro': '몬테네그로',
							'Jordan': '요르단',
							'Latvia': '라트비아',
							'Niger': '니제르',
							'Zimbabwe': '짐바브웨',
							'Liberia': '라이베리아',
							'Uganda': '우간다',
							'Burkina Faso': '부르키나파소',
							'Cyprus': '키프로스',
							'Uruguay': '우루과이',
							'Georgia': '조지아',
							'Namibia': '나미비아',
							'Chad': '차드',
							'Andorra': '안도라',
							'Suriname': '수리남',
							'Jamaica': '자메이카',
							'Togo': '토고',
							'Sao Tome and Principe': '상투메프린시페',
							'San Marino': '산마리노',
							'Malta': '몰타',
							'Réunion': '레위니옹',
							'Channel Islands': '채널제도',
							'Angola': '앙골라',
							'Tanzania': '탄자니아',
							'Syria': '시리아',
							'Taiwan': '대만',
							'Botswana': '보츠와나',
							'Vietnam': '베트남',
							'Mauritius': '모리셔스',
							'Myanmar': '미얀마',
							'Isle of Man': '맨섬',
							'Comoros': '코모로',
							'Guyana': '가이아나',
							'Burundi': '부룬디',
							'Mongolia': '몽골',
							'Lesotho': '레소토',
							'Martinique': '마르티니크섬',
							'Eritrea': '에리트레아',
							'Cayman Islands': '케이맨제도',
							'Guadeloupe': '과들루프섬',
							'Faeroe Islands': '페로스제도',
							'Gibraltar': '지브롤터',
							'Cambodia': '캄보디아',
							'Bermuda': '버뮤다제도',
							'Brunei': '브루나이',
							'Trinidad and Tobago': '트리니다드토바고',
							'Bahamas': '바하마',
							'Monaco': '모나코',
							'Aruba': '아루바',
							'Barbados': '바베이도스',
							'Seychelles': '세이셸',
							'Liechtenstein': '리히텐슈타인',
							'Bhutan': '부탄',
							'Sint Maarten': '신트마르턴',
							'Antigua and Barbuda': '앤티가바부다',
							'Turks and Caicos': '터크스케이커스 제도',
							'Gambia': '감비아',
							'French Polynesia': '프랑스령폴리네시아',
							'Macao': '마카오',
							'Saint Martin': '세인트마틴섬',
							'Belize': '벨리즈',
							'St. Vincent Grenadines': '세인트빈센트그레나딘',
							'Curaçao': '퀴라소',
							'Fiji': '피지',
							'Timor-Leste': '동티모르',
							'Grenada': '그레나다',
							'New Caledonia': '누벨칼레도니섬',
							'Saint Lucia': '세인트루시아',
							'Laos': '라오스',
							'Dominica': '도미니카',
							'Saint Kitts and Nevis': '세인트키츠네비스',
							'Falkland Islands': '포클랜드제도',
							'Greenland': '그린란드',
							'Montserrat': '몬트세랫',
							'Vatican City': '바티칸',
							'Papua New Guinea': '파푸아뉴기니',
							'Western Sahara': '서사하라',
							'Caribbean Netherlands': '카리브 네덜란드',
							'British Virgin Islands': '영국령 버진아일랜드',
							'St. Barth': '생바르텔레미',
							'Anguilla': '앵귈라',
							'Saint Pierre Miquelon': '생피에르미클롱',
                        }
                    },
                ]
            };
        myChart.setOption(option);