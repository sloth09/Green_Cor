# Yearly Simulation 결과 분석 가이드

## 1. Cycles_Available 의미

### 정의
```
Cycles_Available = Total_Shuttles × (8,000시간 / Cycle_Duration_Hours)
```

### 의미
- **이론적 최대 연간 운항 가능 횟수** (모든 shuttle 합산)
- 예: 4척 × (8,000h / 10h) = 800 cycles

### 활용
- `Utilization_Rate = Annual_Cycles / Cycles_Available`
- 실제 운항 횟수가 가용 용량의 몇 %인지 표시

---

## 2. 검증에 필요한 핵심 컬럼 (새로 추가됨)

### A. Cycle Time Breakdown (1회 왕복 시간 분석)
| 컬럼명 | 의미 | 예시 |
|--------|------|------|
| `Cycle_Duration_Hours` | 1회 완전한 왕복 시간 | 9.83h |
| `Shore_Loading_Hours` | 육상 적재 시간 (shuttle_size / 1500) | 3.33h |
| `Pumping_Per_Trip_Hours` | 1회 펌핑 시간 | 2.5h |
| `Travel_Outbound_Hours` | 편도 항해 시간 | 1.0h |
| `Travel_Return_Hours` | 복귀 항해 시간 | 1.0h |
| `Setup_Total_Hours` | 연결/분리 시간 합계 | 2.0h |

**검증 공식:**
```
Cycle_Duration = Shore_Loading + Travel_Outbound + Setup + Pumping + Travel_Return
```

---

### B. Trip Calculation Details (왕복 횟수 계산)

| 컬럼명 | 의미 | Case 1 예시 | Case 2 예시 |
|--------|------|-------------|-------------|
| `Trips_Per_Call` | Vessel 1척당 shuttle 왕복 횟수 | 2 (2500m³ shuttle) | 1 |
| `Vessels_Per_Trip` | Shuttle 1회당 서비스 vessel 수 | 1 | 2 (10000m³ shuttle) |
| `Time_Per_Vessel_Call_Hours` | Vessel 1척 서비스 총 시간 | 13.84h (6.92×2) | 9.83h |

**핵심 차이:**
- **Case 1:** `Trips_Per_Call = ceil(5000 / shuttle_size)`
  - 2500m³ → 2 trips
  - 5000m³ → 1 trip
- **Case 2:** `Vessels_Per_Trip = floor(shuttle_size / 5000)`
  - 10000m³ → 2 vessels

---

### C. Time Analysis (시간 분석)

| 컬럼명 | 계산 공식 | 의미 |
|--------|-----------|------|
| `Total_Hours_Needed` | `Annual_Cycles × Cycle_Duration` | 연간 필요한 총 운항 시간 |
| `Total_Hours_Available` | `Total_Shuttles × 8,000` | 연간 가용 총 시간 |
| `Hours_Per_Shuttle_Used` | `Total_Hours_Needed / Total_Shuttles` | Shuttle 1척당 실제 사용 시간 |
| `Cycles_Per_Shuttle` | `Annual_Cycles / Total_Shuttles` | Shuttle 1척당 연간 운항 횟수 |

**검증 공식:**
```
Required_Shuttles = ceil(Total_Hours_Needed / 8,000)
Utilization_Rate = Total_Hours_Needed / Total_Hours_Available
```

---

## 3. 5000m³ vs 2500m³ Shuttle 비교 검증

### 2050년 예상 결과 (Demand ≈ 15,000,000 m³)

#### 5000m³ Shuttle + 2000m³/h Pump

| 항목 | 값 | 계산 |
|------|-----|------|
| Annual_Calls | 3,000 | 15,000,000 / 5,000 |
| Trips_Per_Call | **1** | ceil(5,000 / 5,000) |
| Annual_Cycles | **3,000** | 3,000 × 1 |
| Cycle_Duration_Hours | 9.83 | (5000/1500) + 1.0 + 2.5 + 2.0 + 1.0 |
| Total_Hours_Needed | **29,490** | 3,000 × 9.83 |
| Total_Shuttles | **4** | ceil(29,490 / 8,000) |
| Hours_Per_Shuttle_Used | 7,373 | 29,490 / 4 |
| Utilization_Rate | 92.2% | 29,490 / 32,000 |

#### 2500m³ Shuttle + 2000m³/h Pump

| 항목 | 값 | 계산 |
|------|-----|------|
| Annual_Calls | 3,000 | 15,000,000 / 5,000 |
| Trips_Per_Call | **2** | ceil(5,000 / 2,500) |
| Annual_Cycles | **6,000** | 3,000 × 2 |
| Cycle_Duration_Hours | 6.92 | (2500/1500) + 1.0 + 1.25 + 2.0 + 1.0 |
| Total_Hours_Needed | **41,520** | 6,000 × 6.92 |
| Total_Shuttles | **6** | ceil(41,520 / 8,000) |
| Hours_Per_Shuttle_Used | 6,920 | 41,520 / 6 |
| Utilization_Rate | 86.5% | 41,520 / 48,000 |

---

## 4. 핵심 인사이트

### 왜 2500m³가 더 많은 척수가 필요한가?

1. **Trips_Per_Call이 2배** → Annual_Cycles가 2배
2. **Cycle_Duration은 70%** (6.92 vs 9.83)
3. **Total_Hours_Needed = 6,000 × 6.92 = 41,520h**
   - 5000m³: 3,000 × 9.83 = 29,490h
   - **41% 더 많은 시간 필요!**

### 비용 차이 원인

| 비용 항목 | 5000m³ (4척) | 2500m³ (6척) | 차이 |
|-----------|--------------|--------------|------|
| CAPEX | 4척 × 단가 | 6척 × 단가 | +50% |
| Fixed OPEX | 4척 × 유지비 | 6척 × 유지비 | +50% |
| Shuttle Fuel | 3,000 cycles | 6,000 cycles | +100% |
| Pump Energy | 3,000 calls | 3,000 calls | 동일 |

**결론:** 작은 shuttle은 더 많은 왕복으로 인해 CAPEX, OPEX, Fuel 모두 증가

---

## 5. 검증 체크리스트

### Excel/CSV에서 확인할 공식들

```excel
# 1. Cycle time 검증
Cycle_Duration = Shore_Loading + Travel_Outbound + Pumping_Per_Trip + Setup_Total + Travel_Return

# 2. Annual cycles 검증
Annual_Cycles = Annual_Calls × Trips_Per_Call

# 3. Total hours 검증
Total_Hours_Needed = Annual_Cycles × Cycle_Duration

# 4. Fleet sizing 검증
Required_Shuttles = CEILING(Total_Hours_Needed / 8000)

# 5. Utilization 검증
Utilization_Rate = Total_Hours_Needed / Total_Hours_Available
Utilization_Rate = Annual_Cycles / Cycles_Available

# 6. Cycles available 검증
Cycles_Available = Total_Shuttles × (8000 / Cycle_Duration)

# 7. Per-shuttle metrics 검증
Hours_Per_Shuttle_Used = Total_Hours_Needed / Total_Shuttles
Cycles_Per_Shuttle = Annual_Cycles / Total_Shuttles
```

---

## 6. 실행 방법

### config/base.yaml 설정
```yaml
execution:
  run_mode: "yearly_simulation"
  single_case: "case_1"
  single_scenario_shuttle_cbm: 5000  # 또는 2500
  single_scenario_pump_m3ph: 2000
```

### 실행
```bash
python main.py
```

### 결과 파일
```
results/yearly_simulation_case_1_5000_2000_[timestamp].csv
```

---

## 7. 새로 추가된 컬럼 활용 예시

### 시간 효율성 분석
```python
# Vessel 1척당 서비스 시간 비교
Time_Per_Vessel_Call_Hours = Cycle_Duration × Trips_Per_Call

# 5000m³: 9.83 × 1 = 9.83h
# 2500m³: 6.92 × 2 = 13.84h
# → 2500m³가 41% 더 오래 걸림
```

### 가동률 분석
```python
# Shuttle 1척당 연간 사용 시간
Hours_Per_Shuttle_Used / 8000 = 개별 가동률

# 5000m³: 7,373 / 8,000 = 92.2%
# 2500m³: 6,920 / 8,000 = 86.5%
```

### 비용 효율성 분석
```python
# 척당 연간 비용
Total_Year_Cost_USDm / Total_Shuttles

# Shuttle fuel 비용
VariableOPEX_Shuttle_USDm ∝ Annual_Cycles
```
