# SeoulCongestedStreaming

## 서울 시 실시간 도시 혼잡도 작성
- 인구별 혼잡도
- 나이별 인구 비율
- 해당 지역 인구 비율
- 교통 수단 찾아보기 
```
28  ROAD_TRAFFIC_STTS	도로소통현황{ 
    29	ROAD_TRAFFIC_SPD	전체도로소통평균속도
    30	ROAD_TRAFFIC_IDX	전체도로소통평균현황
    31	ROAD_TRAFFIC_TIME	도로소통현황 업데이트 시간
    32	ROAD_MSG	전체도로소통평균현황 메세지
    33	LINK_ID	도로구간 LINK ID
    34	ROAD_NM	도로명
    // 35	START_ND_CD	도로노드시작지점 코드
    // 36	START_ND_NM	도로노드시작명
    37	START_ND_XY	도로노드시작지점좌표
    // 38	END_ND_CD	도로노드종료지점 코드
    39	END_ND_NM	도로노드종료명
    40	END_ND_XY	도로노드종료지점좌표
    // 41	DIST	도로구간길이
    42	SPD	도로구간평균속도
    43	IDX	도로구간소통지표
}

61	SUB_STTS	지하철 실시간 도착 현황 {
    62	SUB_STN_NM	지하철역명
    63	SUB_STN_LINE	지하철역 호선
    64	SUB_STN_RADDR	지하철역 도로명 주소
    65	SUB_STN_JIBUN	지하철역 구 지번주소
    66	SUB_STN_X	지하철역 X 좌표(경도)
    67	SUB_STN_Y	지하철역 Y 좌표(위도)
    68	SUB_NT_STN	다음역 코드
    69	SUB_BF_STN	이전역 코드
    70	SUB_ROUTE_NM	지하철노선명
    71	SUB_LINE	지하철호선
    72	SUB_ORD	도착예정열차순번
    73	SUB_DIR	지하철방향
    74	SUB_TERMINAL	종착역
    75	SUB_ARVTIME	열차 도착 시간
    76	SUB_ARMG1	열차 도착 메세지
    77	SUB_ARMG2	열차 도착 메세지
    78	SUB_ARVINFO	열차 도착 코드 정보
}

79	BUS_STN_STTS	버스정류소 현황 {
    80	BUS_STN_ID	정류소ID
    81	BUS_ARS_ID	정류소 고유번호
    82	BUS_STN_NM	정류소명
}

85	RTE_STN_NM	노선 조회 기준 정류장명 {
86	RTE_NM	노선명
87	RTE_ID	노선ID
88	RTE_SECT	노선구간
89	RTE_CONGEST	노선혼잡도
}

92	ACDNT_CNTRL_STTS	사고통제현황 {
93	ACDNT_OCCR_DT	사고발생일시
94	EXP_CLR_DT	통제종료예정일시
95	ACDNT_TYPE	사고발생유형
96	ACDNT_DTYPE	사고발생세부유형
97	ACDNT_INFO	사고통제내용
}

```


