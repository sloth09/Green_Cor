# MILPmodel_v17_250810.py
# 작성: 2025-08-10 (콜 기반/Tank 30K, cycle=Travel+2*(Setup+Pump))
import os
import glob
from math import ceil
import pulp
import numpy as np
import pandas as pd

print("== MILP v17 (콜 기반/Tank 30K) 시작 ==")  # 표기만 v17로 변경

# =========================
# OPTIONS
# =========================
MAKE_PLOTS      = True        # 그림 생성 여부(True/False)
PLOT_TOP_N      = 10          # NPC 최소 상위 N개만 그림
PLOTS_DIR       = "plots"     # 그림 저장 폴더
ROUND_DIGITS    = 2           # CSV 숫자 반올림 자리수
MAX_CALL_HOURS  = 72.0        # 1회 벙커링(Call) 완료 시간 제약
MILLION         = 1e6         # 금액 단위 변환 (USD -> 백만 USD)

# 콜 정의: 한 번 접안 시 몇 항차분을 급유할 것인지
k_voyages_per_call = 1        # 기본 1항차 분(필요 시 2,3으로 변경)

# 항만 이동 2h 해석: 왕복 시간으로 사용함
TRAVEL_IS_ROUNDTRIP = False   # v17 수정: 이동 1회 처리(기존 True → False)

# =========================
# 1) 입력 파라미터
# =========================
hull_types_cbm  = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
pump_types_m3ph = [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
years = list(range(2030, 2051))  # 2030~2050

# 경제/운전 파라미터
r = 0.07                          # 할인율
P_fuel = 600.0                    # USD/ton
sfoc = 379.0                      # g/kWh
H_max = 8000.0                    # hr/year (가동률 반영치)
T_setup = 0.5                     # hr (호스 연결/분리/퍼징)
T_travel_for_shuttle = 2.0        # hr (항만 이동, 편도)
transport_safety_factor = 1.00    # 중복 보수 방지
beta = 2.0                        # 탱크 여유계수
F_peak = 1.5                      # 일일 피크 계수
voyages_per_year = 12             # 선박 1척 연간 항차수

# 밀도
rho_nh3_s    = 0.680              # ton/m3 (storage)
rho_nh3_bunk = 0.681              # ton/m3 (bunkering)

# 수요 성장(선박 수)
start_vessels, end_vessels = 50, 500
vessel_growth = {t: int(round(start_vessels + (end_vessels - start_vessels) * ((t - 2030) / 20.0))) for t in years}

# 항차당 연료량 → m3 (상수 3175 대신 수식 사용)
kg_per_voyage = 2_158_995.0
m3_per_voyage = kg_per_voyage / (rho_nh3_s * 1000.0)   # ≈ 3175 m3/항차

# 1회 벙커링 콜 당 목표 급유량 (k 항차 분)
BUNKER_VOL_PER_CALL_M3 = k_voyages_per_call * m3_per_voyage

# 연간 총수요(m3/yr)
D_annual = {t: vessel_growth[t] * m3_per_voyage * voyages_per_year for t in years}  

# 셔틀 MCR (kW) 
MCR_map = {
    500: 1296,
    1000: 1341,
    1500: 1385,
    2000: 1429,
    2500: 1473,
    3000: 1517,
    3500: 1562,
    4000: 1606
}

# 펌프 전력 (ΔP=4 barg, η=0.7)
DeltaP   = 4.0 * 1e5    # Pa
eta_pump = 0.7
pump_power_kW = {q: (DeltaP * (q / 3600.0)) / eta_pump / 1000.0 for q in pump_types_m3ph}  # kW
C_per_kW = 2000.0
pump_capex = {q: pump_power_kW[q] * C_per_kW for q in pump_types_m3ph}

# 셔틀 CAPEX scaling
ref_capex = 61_500_000.0
ref_size  = 40_000.0
alpha     = 0.75
shuttle_capex       = {i: ref_capex * (i / ref_size)**alpha for i in hull_types_cbm}
shuttle_fixed_opex  = {i: shuttle_capex[i] * 0.05 for i in hull_types_cbm}
shuttle_equip       = {i: shuttle_capex[i] * 0.03 for i in hull_types_cbm}

# 벙커링 시스템 CAPEX & fOPEX
bunkering_capex      = {(i, j): shuttle_equip[i] + pump_capex[j] for i in hull_types_cbm for j in pump_types_m3ph}
bunkering_fixed_opex = {(i, j): bunkering_capex[(i, j)] * 0.05 for i in hull_types_cbm for j in pump_types_m3ph}

# 탱크 시스템
V_tank_ton  = 30_000.0
V_tank_kg   = V_tank_ton * 1000.0
C_tank_per_kg = 1.215
C_tank_each  = C_tank_per_kg * V_tank_kg
tank_fixed_opex_each = C_tank_each * 0.03
E_kwh_per_kg = 0.0378
P_elec       = 0.0769
tank_variable_opex_each = V_tank_kg * E_kwh_per_kg * P_elec
V_tank_m3    = V_tank_kg / (rho_nh3_s * 1000.0)

# =========================
# 2) 결과 저장 구조
# =========================
per_year_rows = []
scenario_rows = []

# =========================
# 3) 시나리오 루프 (콜 기반)
# =========================
for i in hull_types_cbm:
    for j in pump_types_m3ph:

        # 시간 구성요소
        travel_hours_per_cycle = (2.0 * T_travel_for_shuttle) if TRAVEL_IS_ROUNDTRIP else T_travel_for_shuttle
        pumping_time_hr_cycle  = 2.0 * (i / j)                      # v17 수정: 사이클당 펌핑시간 = 로딩+언로딩 2회
        pumping_time_hr_call   = 2.0 * (BUNKER_VOL_PER_CALL_M3 / j) # v17 수정: 콜당 펌핑시간 = 로딩+언로딩 2회
        trips_needed_per_call  = int(ceil(BUNKER_VOL_PER_CALL_M3 / i))

        # 1회 벙커링(Call) 완료 시간 = 트립(사이클) 이동/세팅 × trips + 콜 펌핑시간
        T_call = trips_needed_per_call * (travel_hours_per_cycle + 2.0 * T_setup) + pumping_time_hr_call

        # 사이클 시간(연간 물리 한계)
        T_cycle = travel_hours_per_cycle + 2.0 * T_setup + pumping_time_hr_cycle

        # 72h 사전 필터: 콜 기준
        if T_call > MAX_CALL_HOURS:
            print(f"[사전제외] H={i}cbm, P={j}m3/h: T_call={T_call:.2f}h > {MAX_CALL_HOURS}h (Trips/call={trips_needed_per_call})")
            continue

        # 연료(사이클/콜) – 이동은 사이클, 펌핑은 콜
        shuttle_fuel_ton_per_cycle = (MCR_map[i] * sfoc * travel_hours_per_cycle) / 1e6
        shuttle_fuel_USD_per_cycle = shuttle_fuel_ton_per_cycle * P_fuel

        # 펌프 연료(전력→연료 환산). 기존의 ×2.0 제거(위에서 펌핑시간을 2배 반영했기 때문)
        pump_fuel_ton_per_call = (pump_power_kW[j] * pumping_time_hr_call * sfoc) / 1e6   # ★ v17 수정: *2.0 제거
        pump_fuel_USD_per_call = pump_fuel_ton_per_call * P_fuel

        # 단가
        shuttle_CAPEX_each = shuttle_capex[i]
        shuttle_fOPEX_each = shuttle_fixed_opex[i]
        bunk_CAPEX_each    = bunkering_capex[(i, j)]
        bunk_fOPEX_each    = bunkering_fixed_opex[(i, j)]
        tank_CAPEX_each    = C_tank_each
        tank_fOPEX_each    = tank_fixed_opex_each
        tank_vOPEX_each    = tank_variable_opex_each

        # -------------------------
        # MILP 구성
        # -------------------------
        prob = pulp.LpProblem(f"Bunkering_CallBased_{i}_{j}", pulp.LpMinimize)

        # 변수
        x = pulp.LpVariable.dicts("NewShuttles", years, lowBound=0, cat='Integer')
        N = pulp.LpVariable.dicts("TotalShuttles", years, lowBound=0, cat='Integer')
        y_calls = pulp.LpVariable.dicts("AnnualCalls", years, lowBound=0, cat='Continuous')
        z = pulp.LpVariable.dicts("NewTanks", years, lowBound=0, cat='Integer')
        Z = pulp.LpVariable.dicts("TotalTanks", years, lowBound=0, cat='Integer')

        # 목적함수 (할인 현재가치)
        obj_terms = []
        for t in years:
            disc = 1.0 / ((1.0 + r) ** (t - 2030))

            # 연간 트립(=사이클) 수 = 콜 수 × 콜당 필요한 트립
            cycles_t = y_calls[t] * trips_needed_per_call

            capex_new = (shuttle_CAPEX_each + bunk_CAPEX_each) * x[t] + (tank_CAPEX_each * z[t])
            f_opex    = shuttle_fOPEX_each * N[t] + bunk_fOPEX_each * N[t] + tank_fOPEX_each * Z[t]
            v_opex    = (shuttle_fuel_USD_per_cycle * cycles_t) + (pump_fuel_USD_per_call * y_calls[t]) + (tank_vOPEX_each * Z[t])

            obj_terms.append(disc * (capex_new + f_opex + v_opex))

        prob += pulp.lpSum(obj_terms)

        # 제약식
        for k, t in enumerate(years):
            if t == years[0]:
                prob += N[t] == x[t]
                prob += Z[t] == z[t]
            else:
                prob += N[t] == N[years[k - 1]] + x[t]
                prob += Z[t] == Z[years[k - 1]] + z[t]

            # 1) 연간 수요 충족 (콜 단위)
            prob += y_calls[t] * BUNKER_VOL_PER_CALL_M3 >= D_annual[t]

            # 2) 작업시간 제약(연간 사이클 물리 한계)
            prob += (y_calls[t] * trips_needed_per_call) * T_cycle <= N[t] * H_max

            # 3) 탱크 용량
            prob += N[t] * i * beta <= Z[t] * V_tank_m3

            # 4) 일일 피크 (양쪽을 일일 규모로 비교)
            left_daily  = (y_calls[t] / 365.0) * BUNKER_VOL_PER_CALL_M3 * F_peak
            right_daily = (N[t] * (H_max / T_cycle) / 365.0) * i
            prob += right_daily >= left_daily

            # 5) (선택) 연간 물류여유 — v12의 5)와 같은 의미이나, 2)와 동치라 생략 가능
            prob += (N[t] * (H_max / T_cycle)) * i >= D_annual[t] * transport_safety_factor

        # 풀기
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        status = pulp.LpStatus[prob.status]
        print(f"[SOLVER] H={i}, P={j} -> {status}")
        if status != 'Optimal':
            continue

        # -------------------------
        # 결과 집계
        # -------------------------
        npc_total = 0.0
        npc_shuttle_CAPEX = npc_shuttle_fOPEX = npc_shuttle_vOPEX = 0.0
        npc_bunk_CAPEX    = npc_bunk_fOPEX    = npc_bunk_vOPEX    = 0.0
        npc_tank_CAPEX    = npc_tank_fOPEX    = npc_tank_vOPEX    = 0.0

        for t in years:
            disc = 1.0 / ((1.0 + r) ** (t - 2030))

            xval = x[t].varValue
            Nval = N[t].varValue
            ycall = y_calls[t].varValue
            zval = z[t].varValue
            Zval = Z[t].varValue

            cycles = ycall * trips_needed_per_call
            cycles_available = Nval * (H_max / T_cycle)
            util_rate = (cycles / cycles_available) if cycles_available > 0 else 0.0

            # CAPEX (할인)
            npc_shuttle_CAPEX += disc * (shuttle_CAPEX_each * xval)
            npc_bunk_CAPEX    += disc * (bunk_CAPEX_each    * xval)
            npc_tank_CAPEX    += disc * (tank_CAPEX_each    * zval)

            # fOPEX (할인)
            npc_shuttle_fOPEX += disc * (shuttle_fOPEX_each * Nval)
            npc_bunk_fOPEX    += disc * (bunk_fOPEX_each    * Nval)
            npc_tank_fOPEX    += disc * (tank_fOPEX_each    * Zval)

            # vOPEX (할인)
            shuttle_v = shuttle_fuel_USD_per_cycle * cycles
            pump_v    = pump_fuel_USD_per_call    * ycall
            npc_shuttle_vOPEX += disc * shuttle_v
            npc_bunk_vOPEX    += disc * pump_v
            npc_tank_vOPEX    += disc * (tank_vOPEX_each * Zval)

            npc_total += disc * (
                (shuttle_CAPEX_each * xval) + (bunk_CAPEX_each * xval) + (tank_CAPEX_each * zval) +
                (shuttle_fOPEX_each * Nval) + (bunk_fOPEX_each * Nval) + (tank_fOPEX_each * Zval) +
                shuttle_v + pump_v + (tank_vOPEX_each * Zval)
            )

            # 공급/수요
            supply_m3 = ycall * BUNKER_VOL_PER_CALL_M3
            demand_m3 = D_annual[t]
            headroom_m3 = supply_m3 - demand_m3

            # --- 연도별 결과 행 (금액: 백만 USD로 기록; 할인/미할인 모두 제공) ---
            per_year_rows.append({
                "Shuttle_Size_cbm": i,
                "Pump_Size_m3ph": j,
                "T_call_hr": round(T_call, 4),
                "T_cycle_hr": round(T_cycle, 4),
                "TripsNeeded_per_Call": int(trips_needed_per_call),
                "Year": t,

                "New_Shuttles": int(round(xval)),
                "Total_Shuttles": int(round(Nval)),
                "Annual_Calls": round(ycall, 4),
                "Trips_per_Call": int(trips_needed_per_call),
                "Annual_Cycles": round(cycles, 4),  # = ycall * trips_needed
                "Annual_Cycles_per_Shuttle": round((cycles / Nval) if Nval > 0 else 0.0, 4),

                "New_Tanks": int(round(zval)),
                "Total_Tanks": int(round(Zval)),

                "Supply_m3": round(supply_m3, 4),
                "Demand_m3": round(demand_m3, 4),
                "Headroom_m3": round(headroom_m3, 4),
                "Cycles_Available": round(cycles_available, 4),
                "Required_Cycles_Total": round(demand_m3 / i, 4),  # 참고용
                "Utilization_Rate": round(util_rate, 6),

                # --- 미할인 연간 비용(백만 USD) ---
                "USDm_shuttle_capex":   (shuttle_CAPEX_each * xval) / MILLION,
                "USDm_bunk_capex":      (bunk_CAPEX_each    * xval) / MILLION,
                "USDm_tank_capex":      (tank_CAPEX_each    * zval) / MILLION,
                "USDm_shuttle_fopex":   (shuttle_fOPEX_each * Nval) / MILLION,
                "USDm_bunk_fopex":      (bunk_fOPEX_each    * Nval) / MILLION,
                "USDm_tank_fopex":      (tank_fOPEX_each    * Zval) / MILLION,
                "USDm_shuttle_vopex":   (shuttle_v) / MILLION,
                "USDm_bunk_vopex":      (pump_v) / MILLION,
                "USDm_tank_vopex":      (tank_vOPEX_each * Zval) / MILLION,
                "USDm_total_year":      ((shuttle_CAPEX_each * xval) + (bunk_CAPEX_each * xval) + (tank_CAPEX_each * zval) +
                                         (shuttle_fOPEX_each * Nval) + (bunk_FOPEX_each := bunk_fOPEX_each) * Nval + (tank_fOPEX_each * Zval) +
                                         shuttle_v + pump_v + (tank_vOPEX_each * Zval)) / MILLION,

                # --- 할인 연간 비용(백만 USD) ---
                "USDm_disc_shuttle_capex":   (disc * shuttle_CAPEX_each * xval) / MILLION,
                "USDm_disc_bunk_capex":      (disc * bunk_CAPEX_each    * xval) / MILLION,
                "USDm_disc_tank_capex":      (disc * tank_CAPEX_each    * zval) / MILLION,
                "USDm_disc_shuttle_fopex":   (disc * shuttle_fOPEX_each * Nval) / MILLION,
                "USDm_disc_bunk_fopex":      (disc * bunk_fOPEX_each    * Nval) / MILLION,
                "USDm_disc_tank_fopex":      (disc * tank_fOPEX_each    * Zval) / MILLION,
                "USDm_disc_shuttle_vopex":   (disc * shuttle_v) / MILLION,
                "USDm_disc_bunk_vopex":      (disc * pump_v) / MILLION,
                "USDm_disc_tank_vopex":      (disc * tank_vOPEX_each * Zval) / MILLION,
                "USDm_disc_total_year":      (disc * ((shuttle_CAPEX_each * xval) + (bunk_CAPEX_each * xval) + (tank_CAPEX_each * zval) +
                                                      (shuttle_fOPEX_each * Nval) + (bunk_fOPEX_each * Nval) + (tank_fOPEX_each * Zval) +
                                                      shuttle_v + pump_v + (tank_vOPEX_each * Zval))) / MILLION
            })

        # --- 시나리오 요약 행 (NPC: 백만 USD) ---
        scenario_rows.append({
            "Shuttle_Size_cbm": i,
            "Pump_Size_m3ph": j,
            "T_call_hr": round(T_call, 4),
            "T_cycle_hr": round(T_cycle, 4),
            "TripsNeeded_per_Call": int(trips_needed_per_call),

            "NPC_Total_USDm": npc_total / MILLION,
            "NPC_Shuttle_CAPEX_USDm": npc_shuttle_CAPEX / MILLION,
            "NPC_Shuttle_fOPEX_USDm": npc_shuttle_fOPEX / MILLION,
            "NPC_Shuttle_vOPEX_USDm": npc_shuttle_vOPEX / MILLION,
            "NPC_Bunkering_CAPEX_USDm": npc_bunk_CAPEX / MILLION,
            "NPC_Bunkering_fOPEX_USDm": npc_bunk_fOPEX / MILLION,
            "NPC_Bunkering_vOPEX_USDm": npc_bunk_vOPEX / MILLION,
            "NPC_Terminal_CAPEX_USDm": npc_tank_CAPEX / MILLION,
            "NPC_Terminal_fOPEX_USDm": npc_tank_fOPEX / MILLION,
            "NPC_Terminal_vOPEX_USDm": npc_tank_vOPEX / MILLION
        })

# =========================
# 4) CSV 저장 (백만 USD, 반올림)
# =========================
df_year = pd.DataFrame(per_year_rows)
df_scn  = pd.DataFrame(scenario_rows)

if not df_scn.empty:
    scn_cols = [
        "Shuttle_Size_cbm","Pump_Size_m3ph",
        "T_call_hr","T_cycle_hr","TripsNeeded_per_Call",
        "NPC_Total_USDm",
        "NPC_Shuttle_CAPEX_USDm","NPC_Bunkering_CAPEX_USDm","NPC_Terminal_CAPEX_USDm",
        "NPC_Shuttle_fOPEX_USDm","NPC_Bunkering_fOPEX_USDm","NPC_Terminal_fOPEX_USDm",
        "NPC_Shuttle_vOPEX_USDm","NPC_Bunkering_vOPEX_USDm","NPC_Terminal_vOPEX_USDm"
    ]
    df_scn = df_scn[scn_cols].copy()
    num_cols = [c for c in df_scn.columns if c.startswith("NPC_")]
    df_scn[num_cols] = df_scn[num_cols].round(ROUND_DIGITS)
    df_scn.sort_values(["NPC_Total_USDm","Shuttle_Size_cbm","Pump_Size_m3ph"], inplace=True)

if not df_year.empty:
    # 정렬 및 반올림
    df_year.sort_values(["Shuttle_Size_cbm","Pump_Size_m3ph","Year"], inplace=True)
    round_cols = [
        "T_call_hr","T_cycle_hr","Annual_Calls","Annual_Cycles","Annual_Cycles_per_Shuttle",
        "Supply_m3","Demand_m3","Headroom_m3","Cycles_Available","Required_Cycles_Total","Utilization_Rate",
        "USDm_shuttle_capex","USDm_bunk_capex","USDm_tank_capex",
        "USDm_shuttle_fopex","USDm_bunk_fopex","USDm_tank_fopex",
        "USDm_shuttle_vopex","USDm_bunk_vopex","USDm_tank_vopex","USDm_total_year",
        "USDm_disc_shuttle_capex","USDm_disc_bunk_capex","USDm_disc_tank_capex",
        "USDm_disc_shuttle_fopex","USDm_disc_bunk_fopex","USDm_disc_tank_fopex",
        "USDm_disc_shuttle_vopex","USDm_disc_bunk_vopex","USDm_disc_tank_vopex","USDm_disc_total_year"
    ]
    df_year[round_cols] = df_year[round_cols].round(ROUND_DIGITS)

# 파일 저장
df_scn.to_csv("MILP_scenario_summary_v17.csv", index=False, encoding="utf-8-sig")  # 파일명만 v17
df_year.to_csv("MILP_per_year_results_v17.csv", index=False, encoding="utf-8-sig")
print("CSV 저장 완료: MILP_scenario_summary_v17.csv / MILP_per_year_results_v17.csv")

# =========================
# 5) (선택) 상위 N개만 플롯
# =========================
if MAKE_PLOTS and not df_scn.empty:
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(PLOTS_DIR, exist_ok=True)
    for p in glob.glob(os.path.join(PLOTS_DIR, "*.png")):
        try:
            os.remove(p)
        except Exception:
            pass

    # ----------------------------------------------------
    # 공통: helper & 라벨/컬럼 정의
    # ----------------------------------------------------
    def set_year_axis(ax):
        """x축을 2030~2050, 5년 간격으로 고정."""
        ticks = list(range(2030, 2051, 5))
        ax.set_xlim(2030, 2050)
        ax.set_xticks(ticks)
        ax.set_xticklabels([str(y) for y in ticks])

    # 누적/스택 그래프에서 사용할 컴포넌트 컬럼과 라벨
    comp_cols_yearly = [
        "USDm_disc_shuttle_capex","USDm_disc_bunk_capex","USDm_disc_tank_capex",
        "USDm_disc_shuttle_fopex","USDm_disc_bunk_fopex","USDm_disc_tank_fopex",
        "USDm_disc_shuttle_vopex","USDm_disc_bunk_vopex","USDm_disc_tank_vopex"
    ]
    comp_cols_npc = [
        "NPC_Shuttle_CAPEX_USDm","NPC_Bunkering_CAPEX_USDm","NPC_Terminal_CAPEX_USDm",
        "NPC_Shuttle_fOPEX_USDm","NPC_Bunkering_fOPEX_USDm","NPC_Terminal_fOPEX_USDm",
        "NPC_Shuttle_vOPEX_USDm","NPC_Bunkering_vOPEX_USDm","NPC_Terminal_vOPEX_USDm"
    ]
    comp_labels = [
        "Shuttle CAPEX","Bunk CAPEX","Tank CAPEX",
        "Shuttle fOPEX","Bunk fOPEX","Tank fOPEX",
        "Shuttle vOPEX","Bunk vOPEX","Tank vOPEX"
    ]

    # ----------------------------------------------------
    # (A) Top-N 각 시나리오: 누적(진짜 누적) 할인 연간 비용 스택
    #     - 파일명: cumNPC_H{H}_P{P}.png
    # ----------------------------------------------------
    topN = df_scn.sort_values("NPC_Total_USDm").head(PLOT_TOP_N).copy()

    for _, s in topN.iterrows():
        i = int(s["Shuttle_Size_cbm"])
        j = int(s["Pump_Size_m3ph"])

        df_y = (
            df_year[(df_year["Shuttle_Size_cbm"] == i) &
                    (df_year["Pump_Size_m3ph"] == j)]
            .copy()
            .sort_values("Year")
        )
        # 연도 정수화 & 누적합 계산
        df_y["Year"] = df_y["Year"].astype(int)
        df_stack = df_y[["Year"] + comp_cols_yearly].set_index("Year").sort_index().cumsum()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.stackplot(df_stack.index, [df_stack[c].values for c in comp_cols_yearly],
                     labels=comp_labels)
        ax.set_title(f"Cumulative discounted costs (M USD) — H{i} / P{j}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Cumulative discounted cost (M USD)")
        set_year_axis(ax)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        ax.grid(axis='y', alpha=0.25)
        plt.tight_layout()
        out_png = os.path.join(PLOTS_DIR, f"cumNPC_H{i}_P{j}.png")
        plt.savefig(out_png, dpi=200)
        plt.close(fig)
        print(f"[PLOT] {out_png}")

    # ----------------------------------------------------
    # (B) Top-10 시나리오: NPC(2030~2050 할인합) 스택 막대
    #     - 라벨 줄바꿈으로 겹침 방지: 'H3500\nP2000'
    #     - 파일명: top10_stack_NPC.png
    # ----------------------------------------------------
    top10 = df_scn.sort_values("NPC_Total_USDm").head(10).copy()
    scen_labels_wrapped = [f"H{int(r.Shuttle_Size_cbm)}\nP{int(r.Pump_Size_m3ph)}"
                           for _, r in top10.iterrows()]
    x = np.arange(len(top10))

    fig, ax = plt.subplots(figsize=(12, 6))
    bottoms = np.zeros(len(top10))
    for comp, label in zip(comp_cols_npc, comp_labels):
        vals = top10[comp].values
        ax.bar(x, vals, bottom=bottoms, label=label)
        bottoms += vals

    ax.set_title("Top-10 scenarios — NPC breakdown (M USD, discounted 2030–2050)")
    ax.set_xticks(x, scen_labels_wrapped)
    ax.set_xlabel("Scenario (H: CBM, P: m³/h)")
    ax.set_ylabel("NPC (M USD)")
    ax.grid(axis='y', alpha=0.3)
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()
    out_png = os.path.join(PLOTS_DIR, "top10_stack_NPC.png")
    plt.savefig(out_png, dpi=200)
    plt.close(fig)
    print(f"[PLOT] {out_png}")

    # ----------------------------------------------------
    # (C) Heat map: Shuttle size × Pump flow → NPC
    #     - 싸면 초록, 비싸면 빨강 (RdYlGn_r)
    #     - 파일명: heatmap_NPC.png
    # ----------------------------------------------------
    hulls = sorted(df_scn["Shuttle_Size_cbm"].unique())
    pumps = sorted(df_scn["Pump_Size_m3ph"].unique())

    mat = np.full((len(hulls), len(pumps)), np.nan, dtype=float)
    idx_map = {(int(r.Shuttle_Size_cbm), int(r.Pump_Size_m3ph)): r.NPC_Total_USDm
               for _, r in df_scn.iterrows()}
    for hi, h in enumerate(hulls):
        for pj, p in enumerate(pumps):
            val = idx_map.get((int(h), int(p)))
            if val is not None:
                mat[hi, pj] = val

    fig, ax = plt.subplots(figsize=(12, 7))
    masked = np.ma.masked_invalid(mat)

    # 싸면 초록, 비싸면 빨강
    cmap = plt.cm.RdYlGn_r
    cmap.set_bad(color='#dddddd')  # NaN 회색

    im = ax.imshow(masked, aspect='auto', cmap=cmap)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("NPC (M USD)")

    ax.set_title("NPC heat map by shuttle size (CBM) and pump flow (m³/h)")
    ax.set_xticks(np.arange(len(pumps)))
    ax.set_xticklabels([str(int(p)) for p in pumps], rotation=0)
    ax.set_yticks(np.arange(len(hulls)))
    ax.set_yticklabels([str(int(h)) for h in hulls])
    ax.set_xlabel("Pump flow (m³/h)")
    ax.set_ylabel("Shuttle size (CBM)")
    plt.tight_layout()
    out_png = os.path.join(PLOTS_DIR, "heatmap_NPC.png")
    plt.savefig(out_png, dpi=200)
    plt.close(fig)
    print(f"[PLOT] {out_png}")

    # ----------------------------------------------------
    # (D) Top-10 시나리오: 연도별 셔틀 총대수 비교 (한 그래프에 10개)
    #     - 파일명: top10_shuttles.png
    # ----------------------------------------------------
    if not df_year.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        for _, r in top10.iterrows():
            i = int(r["Shuttle_Size_cbm"])
            j = int(r["Pump_Size_m3ph"])
            lab = f"H{i}/P{j}"
            df_y = (
                df_year[(df_year["Shuttle_Size_cbm"] == i) &
                        (df_year["Pump_Size_m3ph"] == j)]
                .copy()
                .sort_values("Year")
            )
            df_y["Year"] = df_y["Year"].astype(int)
            ax.plot(df_y["Year"], df_y["Total_Shuttles"], label=lab, linewidth=1.8)

        ax.set_title("Top-10 scenarios — Total shuttles over time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Shuttles (count)")
        set_year_axis(ax)
        ax.grid(True, alpha=0.3)
        ax.legend(ncol=2, fontsize=9, loc='upper left', bbox_to_anchor=(1.0, 1.0))
        plt.tight_layout()
        out_png = os.path.join(PLOTS_DIR, "top10_shuttles.png")
        plt.savefig(out_png, dpi=200)
        plt.close(fig)
        print(f"[PLOT] {out_png}")

print("== 종료: v17 ==")  # 표기만 v17로 변경
