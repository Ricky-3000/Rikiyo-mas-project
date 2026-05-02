import random
import matplotlib.pyplot as plt
import numpy as np

# --- 1. 黄金バランス・パラメータ (計算テストのロジックを完全移植) ---
POPULATION = 5000
IMPACT = random.uniform(0.70, 0.92)      
THRESHOLD_AVG = random.uniform(0.35, 0.45) 

INITIAL_DECAY_PERCENT = random.uniform(0.09, 0.12) 
DECAY_PERCENT = INITIAL_DECAY_PERCENT
DECAY_MIN_BASE = 0.035 

BASE_VIEW_RATE = 0.004
REVIVAL_PROB = random.uniform(0.04, 0.07)
revival_success_count = 0

# --- 2. 初期化 ---
user_thresholds = np.sort(np.random.normal(THRESHOLD_AVG, 0.15, POPULATION))
user_interests = np.random.uniform(0.5, 2.0, POPULATION)
active_users = set()
active_users.add(random.randint(0, POPULATION-1))

steps, new_posts_history, total_posts_history = [1], [1], [1]
freshness = 1.0 
max_momentum = 0
revival_logs = []

def get_status_bar(percent, width=20):
    filled = int(width * percent / 100)
    return "[" + "█" * filled + "░" * (width - filled) + "]"

print("\n" + "🚀 トレンドシミュレーター：黄金バランス統合版 開始 ".center(75, "="))

# --- 3. メインループ ---
step = 1
while True:
    step += 1
    new_posts = 0
    current_reach_p = (len(active_users) / POPULATION) * 100
    
    resistance = 1.0
    if current_reach_p > 20: resistance += (current_reach_p - 20) * 0.008
    if current_reach_p > 60: resistance += (current_reach_p - 60) * 0.02
        
    decay_min = max(0.025, DECAY_MIN_BASE - (revival_success_count * 0.003))
    current_decay = min(0.35, DECAY_PERCENT * resistance)
    
    peer_pressure = 1.0
    if current_reach_p > 75:
        peer_pressure = 1.0 + (current_reach_p - 75) * 0.12
        
    prev_momentum = new_posts_history[-1] * 0.01
    dynamic_view_rate = min(0.09, BASE_VIEW_RATE * (1 + prev_momentum))
    
    for i in range(POPULATION):
        if i not in active_users:
            if random.random() < (dynamic_view_rate * user_interests[i]):
                luck = random.uniform(-0.05, 0.05)
                effective_impact = IMPACT * max(0.25, (1.0 - (current_reach_p / 350))) * peer_pressure
                
                if (effective_impact * freshness) + luck > user_thresholds[i]:
                    active_users.add(i)
                    new_posts += 1
    
    if new_posts > max_momentum: max_momentum = new_posts
    steps.append(step)
    new_posts_history.append(new_posts)
    total_posts_history.append(len(active_users))

    revival_occurred = False
    if random.random() < REVIVAL_PROB:
        quality = random.uniform(0.05, 0.6)
        freshness = min(1.0, freshness + max(0.2, quality))
        
        if quality > 0.15:
            revival_success_count += 1
            DECAY_PERCENT = max(decay_min, DECAY_PERCENT - 0.012)
            BASE_VIEW_RATE = min(0.018, BASE_VIEW_RATE + 0.0018)
        
        revival_type = "🔥好意的" if quality > 0.3 else "☁️並み"
        revival_logs.append({"step": step, "type": revival_type, "reach": current_reach_p})
        revival_occurred = True

    freshness *= (1.0 - current_decay)
    
    if step % 10 == 0 or revival_occurred:
        rev_tag = f" ★再燃({revival_type})" if revival_occurred else ""
        print(f"Step {step:3} | {get_status_bar(current_reach_p)} {current_reach_p:5.1f}% | 新規: {new_posts:3}{rev_tag}")
    
    if len(active_users) >= POPULATION:
        reason = "市場完全制覇（社会現象）"
        break
    if step > 20 and (freshness < 0.025 or (new_posts == 0 and step > 140)):
        reason = "沈静化"
        break
    if step > 2500:
        reason = "時間切れ"
        break

# --- 4. 最終レポート ---
final_count = len(active_users)
print("\n" + "■" * 75)
print(f" 📊 トレンド深層レポート ".center(75, "■"))
print("■" * 75)
print(f" ● 最終到達人数 : {final_count}人 / {POPULATION}人 ({current_reach_p:.1f}%)")
print(f" ● 寿命         : {step} ステップ")
print(f" ● 終了原因     : {reason}")

if current_reach_p < 10: res = "不発"
elif current_reach_p < 35: res = "局地流行"
elif current_reach_p < 65: res = "プチバズ"
elif current_reach_p < 90: res = "ヒット"
else: res = "社会現象"
print(f" ● 最終格付     : 【{res}】")
print("■" * 75 + "\n")

# --- 5. グラフ描画 ---
plt.figure(figsize=(14, 6))

# 左グラフ：勢いの推移
plt.subplot(1, 2, 1)
plt.plot(steps, new_posts_history, color='orange', label='New Users per Step')
plt.fill_between(steps, new_posts_history, color='orange', alpha=0.2)
plt.title(f"Momentum Analysis (Max: {max_momentum})")
plt.xlabel("Steps")
plt.ylabel("New Active Users")
plt.grid(axis='y', alpha=0.3)

# 右グラフ：累計到達（人数を明記）
plt.subplot(1, 2, 2)
plt.plot(steps, total_posts_history, color='dodgerblue', linewidth=2.5, label='Total Reach')
# 到達人数を強調表示
plt.annotate(f'Final: {final_count} users', 
             xy=(steps[-1], total_posts_history[-1]), 
             xytext=(steps[-1]*0.7, total_posts_history[-1]*0.8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
             fontsize=12, fontweight='bold', color='red')

plt.axhline(y=POPULATION * 0.9, color='crimson', linestyle='--', alpha=0.4, label='Social Phenomenon (90%)')
plt.axhline(y=POPULATION * 0.65, color='darkviolet', linestyle='--', alpha=0.4, label='Major Hit (65%)')
plt.axhline(y=POPULATION * 0.35, color='forestgreen', linestyle='--', alpha=0.4, label='Petit Buzz (35%)')

plt.title(f"Total Growth: {final_count} / {POPULATION} ({current_reach_p:.1f}%)")
plt.xlabel("Steps")
plt.ylabel("Cumulative Users")
plt.ylim(0, POPULATION * 1.05)
plt.legend(loc='lower right')
plt.grid(axis='y', alpha=0.2)

plt.tight_layout()
plt.show()