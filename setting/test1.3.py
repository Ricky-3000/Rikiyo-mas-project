import random
import numpy as np

def run_simulation(population=5000):
    # --- 1. 基本パラメータの再調整（地力アップ） ---
    IMPACT = random.uniform(0.68, 0.90) 
    THRESHOLD_AVG = random.uniform(0.35, 0.45) 
    
    INITIAL_DECAY_PERCENT = random.uniform(0.09, 0.12) 
    DECAY_PERCENT = INITIAL_DECAY_PERCENT
    DECAY_MIN = 0.035 # 完走を許容するスタミナ
    
    BASE_VIEW_RATE = 0.004 # 露出の初期値を少しアップ
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
        
        # --- 2. 普及抵抗（マイルド化） ---
        resistance = 1.0
        if current_reach_p > 20:
            resistance += (current_reach_p - 20) * 0.008 # 抵抗をマイルドに
        if current_reach_p > 60:
            resistance += (current_reach_p - 60) * 0.02 # ヒットへの壁
            
        current_decay = min(0.35, DECAY_PERCENT * resistance)
        
        # --- 3. 加速装置（80%からのラストスパート） ---
        peer_pressure = 1.0
        if current_reach_p > 80:
            peer_pressure = 1.0 + (current_reach_p - 80) * 0.1 
            
        prev_momentum = new_posts_history[-1] * 0.01
        dynamic_view_rate = min(0.09, BASE_VIEW_RATE * (1 + prev_momentum))
        
        new_posts = 0
        for i in range(population):
            if i not in active_users:
                if random.random() < (dynamic_view_rate * user_interests[i]):
                    luck = random.uniform(-0.05, 0.05)
                    # 減衰分母を 320 に広げ、地力の寿命を延ばす
                    effective_impact = IMPACT * max(0.2, (1.0 - (current_reach_p / 320))) * peer_pressure
                    
                    if (effective_impact * freshness) + luck > user_thresholds[i]:
                        active_users.add(i)
                        new_posts += 1
        
        new_posts_history.append(new_posts)
        
        # --- 4. 再燃（ブースト復活） ---
        if random.random() < REVIVAL_PROB:
            quality = random.uniform(0.0, 0.6) # 💀を排除
            freshness = min(1.0, freshness + max(0.18, quality))
            if quality > 0.15:
                revival_success_count += 1
                # 改善幅を 0.01 に戻して「完走」のスタミナを与える
                DECAY_PERCENT = max(DECAY_MIN, DECAY_PERCENT - 0.01)
                BASE_VIEW_RATE = min(0.016, BASE_VIEW_RATE + 0.0015)
        
        freshness *= (1.0 - current_decay)
        
        if len(active_users) >= population: return 100.0
        if step > 20 and (freshness < 0.03 or (new_posts == 0 and step > 140)):
            return current_reach_p
        if step > 2500: return current_reach_p

def start_batch_test(trials=1000):
    print(f"\n🚀 {trials}回の「完走ルート再開拓」検証開始...")
    results = []
    for _ in range(trials):
        results.append(run_simulation())
    
    results = np.array(results)
    print("\n" + "="*50)
    print(f" 📊 再検証：統計レポート ".center(50, "="))
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