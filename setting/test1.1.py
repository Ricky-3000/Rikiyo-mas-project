import random
import numpy as np

def run_test_logic(population=5000):
    # --- パラメータ (統合版ロジックを完全再現) ---
    IMPACT = random.uniform(0.70, 0.92)
    THRESHOLD_AVG = random.uniform(0.35, 0.45)
    INITIAL_DECAY = random.uniform(0.09, 0.12)
    DECAY_PERCENT = INITIAL_DECAY
    DECAY_MIN_BASE = 0.035
    BASE_VIEW_RATE = 0.004
    REVIVAL_PROB = random.uniform(0.04, 0.07)
    revival_success_count = 0
    
    user_thresholds = np.sort(np.random.normal(THRESHOLD_AVG, 0.15, population))
    user_interests = np.random.uniform(0.5, 2.0, population)
    active_users = set()
    active_users.add(random.randint(0, population-1))
    
    new_posts_history = [1]
    freshness = 1.0
    step = 0
    
    # 解析用フラグ
    reached_20 = False
    reached_60 = False
    reached_75 = False

    while True:
        step += 1
        current_reach_p = (len(active_users) / population) * 100
        
        # --- 抵抗とブーストの計算 ---
        resistance = 1.0
        if current_reach_p > 20: 
            resistance += (current_reach_p - 20) * 0.008
            reached_20 = True
        if current_reach_p > 60: 
            resistance += (current_reach_p - 60) * 0.02
            reached_60 = True
            
        decay_min = max(0.025, DECAY_MIN_BASE - (revival_success_count * 0.003))
        current_decay = min(0.35, DECAY_PERCENT * resistance)
        
        peer_pressure = 1.0
        if current_reach_p > 75:
            peer_pressure = 1.0 + (current_reach_p - 75) * 0.12
            reached_75 = True
            
        dynamic_view_rate = min(0.09, BASE_VIEW_RATE * (1 + new_posts_history[-1] * 0.01))
        
        new_posts = 0
        for i in range(population):
            if i not in active_users:
                if random.random() < (dynamic_view_rate * user_interests[i]):
                    luck = random.uniform(-0.05, 0.05)
                    eff_impact = IMPACT * max(0.25, (1.0 - (current_reach_p / 350))) * peer_pressure
                    if (eff_impact * freshness) + luck > user_thresholds[i]:
                        active_users.add(i)
                        new_posts += 1
        
        new_posts_history.append(new_posts)
        
        # 再燃判定
        if random.random() < REVIVAL_PROB:
            quality = random.uniform(0.05, 0.6)
            freshness = min(1.0, freshness + max(0.2, quality))
            if quality > 0.15:
                revival_success_count += 1
                DECAY_PERCENT = max(decay_min, DECAY_PERCENT - 0.012)
                BASE_VIEW_RATE = min(0.018, BASE_VIEW_RATE + 0.0018)
        
        freshness *= (1.0 - current_decay)
        
        if len(active_users) >= population: return 100.0, step, revival_success_count
        if step > 20 and (freshness < 0.025 or (new_posts == 0 and step > 140)):
            return current_reach_p, step, revival_success_count
        if step > 2500: return current_reach_p, step, revival_success_count

def start_evidence_test(trials=1000):
    print(f"📊 {trials}回の試行に基づいた「黄金バランス」計算根拠レポートを開始...\n")
    results = []
    for _ in range(trials):
        results.append(run_test_logic())
    
    reaches = np.array([r[0] for r in results])
    revivals = np.array([r[2] for r in results])
    
    # --- 分類集計 ---
    cats = [
        ("社会現象 (90%+)", 90, 101),
        ("ヒット (65-90%)", 65, 90),
        ("プチバズ (35-65%)", 35, 65),
        ("局地流行 (10-35%)", 10, 35),
        ("不発 (10%未満)", 0, 10)
    ]
    
    print("="*60)
    print("【1. トレンド発生確率分布】")
    for name, low, high in cats:
        count = len(reaches[(reaches >= low) & (reaches < high)])
        share = (count / trials) * 100
        bar = "█" * int(share / 2)
        print(f"{name:15} : {share:5.1f}% | {bar}")
    
    print("\n【2. 数学的根拠分析】")
    # 平均再燃成功回数の相関
    avg_rev_phenom = revivals[reaches >= 90].mean() if any(reaches >= 90) else 0
    avg_rev_fail = revivals[reaches < 10].mean() if any(reaches < 10) else 0
    
    print(f" ● 社会現象化に必要な平均再燃回数 : {avg_rev_phenom:.2f} 回")
    print(f" ● 不発に終わる平均再燃回数       : {avg_rev_fail:.2f} 回")
    print(f" ● キャズム（20%）突破難易度係数   : 0.008 (緩やか)")
    print(f" ● マジョリティ（60%）抵抗係数     : 0.020 (強力)")
    print(f" ● 最終局面（75%）同調加速係数     : 0.120 (極めて強力)")
    
    print("\n【3. 結論：このロジックの性質】")
    if avg_rev_phenom > avg_rev_fail * 2:
        print(" >>> 「質の高い続報（再燃）」が完走の決定的要因となっています。")
    print(f" >>> 到達率の平均は {reaches.mean():.1f}% であり、中間層がバランス良く生成されます。")
    print("="*60)

if __name__ == "__main__":
    start_evidence_test(1000)