import random
import numpy as np

def run_simulation(population=5000):
    IMPACT = random.uniform(0.70, 0.92) # 地力をさらに微増
    THRESHOLD_AVG = random.uniform(0.35, 0.45) 
    
    INITIAL_DECAY_PERCENT = random.uniform(0.09, 0.12) 
    DECAY_PERCENT = INITIAL_DECAY_PERCENT
    DECAY_MIN_BASE = 0.035 
    
    BASE_VIEW_RATE = 0.004
    REVIVAL_PROB = random.uniform(0.04, 0.07)
    revival_success_count = 0
    
    user_thresholds = np.sort(np.random.normal(THRESHOLD_AVG, 0.15, population))
    user_interests = np.random.uniform(0.5, 2.0, population)
    freshness = 1.0
    active_users = set()
    active_users.add(random.randint(0, population-1))
    
    new_posts_history = [1]
    step = 0
    
    while True:
        step += 1
        current_reach_p = (len(active_users) / population) * 100
        
        # 普及抵抗（現状維持）
        resistance = 1.0
        if current_reach_p > 20: resistance += (current_reach_p - 20) * 0.008
        if current_reach_p > 60: resistance += (current_reach_p - 60) * 0.02
            
        # 再燃回数に応じて飽きの限界値を下げる（延命処置）
        decay_min = max(0.025, DECAY_MIN_BASE - (revival_success_count * 0.003))
        current_decay = min(0.35, DECAY_PERCENT * resistance)
        
        # 【修正】同調圧力：発動を 75% に早め、倍率も微増
        peer_pressure = 1.0
        if current_reach_p > 75:
            peer_pressure = 1.0 + (current_reach_p - 75) * 0.12
            
        prev_momentum = new_posts_history[-1] * 0.01
        dynamic_view_rate = min(0.09, BASE_VIEW_RATE * (1 + prev_momentum))
        
        new_posts = 0
        for i in range(population):
            if i not in active_users:
                if random.random() < (dynamic_view_rate * user_interests[i]):
                    luck = random.uniform(-0.05, 0.05)
                    # 【修正】最低威力を 0.25 に。分母を 350 に。
                    effective_impact = IMPACT * max(0.25, (1.0 - (current_reach_p / 350))) * peer_pressure
                    
                    if (effective_impact * freshness) + luck > user_thresholds[i]:
                        active_users.add(i)
                        new_posts += 1
        
        new_posts_history.append(new_posts)
        
        # 再燃
        if random.random() < REVIVAL_PROB:
            quality = random.uniform(0.05, 0.6) # 質の底上げ
            freshness = min(1.0, freshness + max(0.2, quality))
            if quality > 0.15:
                revival_success_count += 1
                DECAY_PERCENT = max(decay_min, DECAY_PERCENT - 0.012) # 改善幅を強化
                BASE_VIEW_RATE = min(0.018, BASE_VIEW_RATE + 0.0018)
        
        freshness *= (1.0 - current_decay)
        
        if len(active_users) >= population: return 100.0
        if step > 20 and (freshness < 0.025 or (new_posts == 0 and step > 140)):
            return current_reach_p
        if step > 2500: return current_reach_p

def start_batch_test(trials=1000):
    print(f"\n🚀 {trials}回の最終バランス（社会現象解禁）検証開始...")
    results = []
    for _ in range(trials):
        results.append(run_simulation())
    
    results = np.array(results)
    print("\n" + "="*50)
    print(f" 📊 究極バランス：統計レポート ".center(50, "="))
    print("="*50)
    
    cats = [
        ("社会現象 (90%+)", 90, 101),
        ("ヒット (65-90%)", 65, 90),
        ("プチバズ (35-65%)", 35, 65),
        ("局地流行 (10-35%)", 10, 35),
        ("不発 (10%未満)", 0, 10)
    ]
    
    for name, low, high in cats:
        count = len(results[(results >= low) & (results < high)])
        share = (count / trials) * 100
        print(f"{name:15} : {share:5.1f}% | {'█' * int(share/2)}")
    
    print("-" * 50)
    print(f" 平均到達率 : {results.mean():.1f}% | 最高到達率 : {results.max():.1f}%")
    print("="*50 + "\n")

if __name__ == "__main__":
    start_batch_test(1000)