import random
import numpy as np

def run_simulation(population=5000):
    # --- 【黄金比：プチバズと完走の両立】 ---
    IMPACT = random.uniform(0.65, 0.88) 
    THRESHOLD_AVG = random.uniform(0.35, 0.45) 
    
    INITIAL_DECAY_PERCENT = random.uniform(0.10, 0.13) 
    DECAY_PERCENT = INITIAL_DECAY_PERCENT
    DECAY_MIN = 0.038 # 完走のためのスタミナを確保
    
    BASE_VIEW_RATE = 0.0035
    REVIVAL_PROB = random.uniform(0.04, 0.07) 
    REVIVAL_LIMIT = 0.40
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
        new_posts = 0
        current_reach_p = (len(active_users) / population) * 100
        
        # 普及抵抗：20%から開始するが、再燃回数に応じて「慣性」で緩和
        resistance_factor = 0.02 - (revival_success_count * 0.002) # 再燃するほど坂が緩やかに
        resistance = 1.0
        if current_reach_p > 20:
            resistance = 1.0 + (current_reach_p - 20) * max(0.005, resistance_factor)
        current_decay = min(0.35, DECAY_PERCENT * resistance)
        
        # 露出の慣性
        prev_momentum = new_posts_history[-1] * 0.01
        dynamic_view_rate = min(0.08, BASE_VIEW_RATE * (1 + prev_momentum))
        
        for i in range(population):
            if i not in active_users:
                if random.random() < (dynamic_view_rate * user_interests[i]):
                    luck = random.uniform(-0.05, 0.05)
                    
                    # 【新ロジック】同調圧力：普及率が極めて高いとインパクトが再加速
                    peer_pressure = 1.0 + (current_reach_p / 100) * 0.2 if current_reach_p > 70 else 1.0
                    effective_impact = IMPACT * max(0.2, (1.0 - (current_reach_p / 300))) * peer_pressure
                    
                    if (effective_impact * freshness) + luck > user_thresholds[i]:
                        active_users.add(i)
                        new_posts += 1
        
        new_posts_history.append(new_posts)
        
        # 再燃：質の高い再燃は社会構造を恒久的に変える
        if random.random() < REVIVAL_PROB:
            quality = random.uniform(-0.02, 0.55)
            freshness = min(1.0, freshness + max(0.2, quality))
            if quality > 0.15:
                revival_success_count += 1
                BASE_VIEW_RATE = min(0.016, BASE_VIEW_RATE + 0.0015)
                DECAY_PERCENT = max(DECAY_MIN, DECAY_PERCENT - 0.01)
            REVIVAL_PROB = max(0.02, min(REVIVAL_LIMIT, REVIVAL_PROB + (quality * 0.04)))
            
        freshness *= (1.0 - current_decay)
        
        if len(active_users) >= population: return 100.0
        if step > 20 and (freshness < 0.03 or (new_posts == 0 and step > 140)):
            return current_reach_p
        if step > 2500: return current_reach_p

def start_batch_test(trials=1000):
    print(f"\n🚀 {trials}回の最終バランス検証を開始...")
    results = []
    for _ in range(trials):
        results.append(run_simulation())
    
    results = np.array(results)
    
    print("\n" + "="*50)
    print(f" 📊 最終統計レポート (1000回試行) ".center(50, "="))
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
        bar = "█" * int(share / 2)
        print(f"{name:15} : {share:5.1f}% | {bar}")
    
    print("-" * 50)
    print(f" 平均到達率 : {results.mean():.1f}% | 最高到達率 : {results.max():.1f}%")
    print("="*50 + "\n")

if __name__ == "__main__":
    start_batch_test(1000)