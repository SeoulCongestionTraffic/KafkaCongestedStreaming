# SeoulCongestedStreaming

## 서울 시 실시간 인구혼잡도 평균 계산 작성

### architecture 
<img width="1190" alt="image" src="https://github.com/SeoulCongestionTraffic/SeoulCongestedStreaming/assets/52487610/7ca04d12-084f-4c47-b6f8-1d9680ca2811">


### 서울시 도시혼잡도 URL 
- https://data.seoul.go.kr/SeoulRtd/

### 실시간 인구 API 
- https://data.seoul.go.kr/dataList/OA-21778/A/1/datasetView.do
```
| No  | 출력명                  | 출력설명                                     
| --- | ---------------------- | -----------------------------------------|       
| 1   | AREA_NM                | 핫스팟 장소명                                
| 2   | AREA_CD                | 핫스팟 코드명                               
| 3   | LIVE_PPLTN_STTS        | 실시간 인구현황                             
| 4   | AREA_CONGEST_LVL       | 장소 혼잡도 지표                            
| 5   | AREA_CONGEST_MSG       | 장소 혼잡도 지표 관련 메세지                   
| 6   | AREA_PPLTN_MIN         | 실시간 인구 지표 최소값                       
| 7   | AREA_PPLTN_MAX         | 실시간 인구 지표 최대값                       
| 8   | MALE_PPLTN_RATE        | 남성 인구 비율(남성)                         
| 9   | FEMALE_PPLTN_RATE      | 여성 인구 비율(여성)                         
| 10  | PPLTN_RATE_0           | 0~10세 인구 비율                           
| 11  | PPLTN_RATE_10          | 10대 실시간 인구 비율                        
| 12  | PPLTN_RATE_20          | 20대 실시간 인구 비율                        
| 13  | PPLTN_RATE_30          | 30대 실시간 인구 비율                        
| 14  | PPLTN_RATE_40          | 40대 실시간 인구 비율                        
| 15  | PPLTN_RATE_50          | 50대 실시간 인구 비율                        
| 16  | PPLTN_RATE_60          | 60대 실시간 인구 비율                        
| 17  | PPLTN_RATE_70          | 70대 실시간 인구 비율                        
| 18  | RESNT_PPLTN_RATE       | 상주 인구 비율                             
| 19  | NON_RESNT_PPLTN_RATE   | 비상주 인구 비율                            
| 20  | REPLACE_YN             | 대체 데이터 여부                            
| 21  | PPLTN_TIME             | 실시간 인구 데이터 업데이트 시간               
| 22  | FCST_YN                | 예측값 제공 여부                          
| 23  | FCST_PPLTN             | 인구 예측 오브젝트                          
| 24  | FCST_TIME              | 인구 예측시점                             
| 25  | FCST_CONGEST_LVL       | 장소 예측 혼잡도 지표                    
| 26  | FCST_PPLTN_MIN         | 예측 실시간 인구 지표 최소값              
| 27  | FCST_PPLTN_MAX         | 예측 실시간 인구 지표 최대값              
```


### 현재 진행중(스키마 정제중)
- 인구별 혼잡도
- 나이별 인구 비율
- 해당 지역 인구 비율


