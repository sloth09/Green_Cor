#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v2.4 최적 시나리오 추출 스크립트
각 case의 최적 shuttle/pump 조합과 Top 5, Worst 3 시나리오 추출
"""

import pandas as pd
from pathlib import Path

results_dir = Path("../../results")

cases = ['case_1', 'case_2_ulsan', 'case_2_yeosu']

for case_id in cases:
    csv_path = results_dir / f"MILP_scenario_summary_{case_id}.csv"

    if not csv_path.exists():
        print(f"[ERROR] {csv_path} not found")
        continue

    df = pd.read_csv(csv_path)

    # 최적해 (최저 NPC)
    best_idx = df['NPC_Total_USDm'].idxmin()
    best = df.loc[best_idx]

    # Top 5
    top5 = df.nsmallest(5, 'NPC_Total_USDm')

    # Worst 3
    worst3 = df.nlargest(3, 'NPC_Total_USDm')

    print(f"\n{'='*80}")
    print(f"CASE: {case_id}")
    print(f"{'='*80}")

    print(f"\n[OPTIMAL SOLUTION]")
    print(f"  Shuttle: {int(best['Shuttle_Size_cbm'])} m³")
    print(f"  Pump: {int(best['Pump_Size_m3ph'])} m³/h")
    print(f"  LCOAmmonia: ${best['LCOAmmonia_USD_per_ton']:.2f}/ton")
    print(f"  NPC Total: ${best['NPC_Total_USDm']:.2f}M")
    print(f"  Cycle Time: {best['Cycle_Duration_hr']:.2f} hr")
    print(f"  Trips per Call: {int(best['Trips_per_Call'])}")
    print(f"  Annual Cycles Max: {best['Annual_Cycles_Max']:.0f}")

    print(f"\n[TOP 5 SCENARIOS]")
    for rank, (idx, row) in enumerate(top5.iterrows(), 1):
        print(f"  {rank}. Shuttle={int(row['Shuttle_Size_cbm'])} × Pump={int(row['Pump_Size_m3ph'])}: "
              f"LCO=${row['LCOAmmonia_USD_per_ton']:.2f}/ton, NPC=${row['NPC_Total_USDm']:.2f}M")

    print(f"\n[WORST 3 SCENARIOS]")
    for rank, (idx, row) in enumerate(worst3.iterrows(), 1):
        print(f"  {rank}. Shuttle={int(row['Shuttle_Size_cbm'])} × Pump={int(row['Pump_Size_m3ph'])}: "
              f"LCO=${row['LCOAmmonia_USD_per_ton']:.2f}/ton, NPC=${row['NPC_Total_USDm']:.2f}M (Issue: High cost)")

    # 이 케이스의 Shuttle/Pump별 샘플 출력
    print(f"\n[SHUTTLE SIZE TRADE-OFF @ Best Pump={int(best['Pump_Size_m3ph'])} m³/h]")
    best_pump = int(best['Pump_Size_m3ph'])
    pump_filtered = df[df['Pump_Size_m3ph'] == best_pump].sort_values('Shuttle_Size_cbm')
    for _, row in pump_filtered.head(7).iterrows():
        print(f"  {int(row['Shuttle_Size_cbm']):>5} m³ | Trips={int(row['Trips_per_Call'])}, "
              f"Cycle={row['Cycle_Duration_hr']:>6.2f}hr, LCO=${row['LCOAmmonia_USD_per_ton']:>5.2f}/ton")

    print(f"\n[PUMP RATE TRADE-OFF @ Best Shuttle={int(best['Shuttle_Size_cbm'])} m³]")
    best_shuttle = int(best['Shuttle_Size_cbm'])
    shuttle_filtered = df[df['Shuttle_Size_cbm'] == best_shuttle].sort_values('Pump_Size_m3ph')
    for _, row in shuttle_filtered.iterrows():
        print(f"  {int(row['Pump_Size_m3ph']):>4} m³/h | Pumping={row['Pumping_Per_Vessel_hr']:.2f}hr, "
              f"Cycle={row['Cycle_Duration_hr']:>6.2f}hr, LCO=${row['LCOAmmonia_USD_per_ton']:>5.2f}/ton")

print("\n" + "="*80)
print("[OK] 최적 시나리오 추출 완료")
print("="*80)
