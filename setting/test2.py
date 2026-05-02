import random
import matplotlib.pyplot as plt
import numpy as np

# --- 1. 設定（カオスと残酷な現実の導入） ---
POPULATION = 5000

# 【運命】マーケット・フィット：このネタが世間に受ける素質 (0.3〜1.2)
# これが低いと、どんなインフルエンサーが叫んでも「内輪ノリ」で終わる
MARKET_FIT = random.uniform(0.3, 1.2) 
IMPACT = random.uniform(0.3, 0.7) * MARKET_FIT

# 【格差】しきい値のばらつきを大きくし「超・保守層」を大量生成
THRESHOLD_AVG = random.uniform(0.4, 0.6) 
user_thresholds = np.random.normal(THRESHOLD_AVG, 0.25, POPULATION)
# 【感度】個人の興味も極端に（一部のオタクと、大多数の無関心）
user_interests = np.random.lognormal(0, 0.6, POPULATION) 

INITIAL_DECAY_PERCENT = random.uniform(0.1, 0.2) # 飽きられる速度は速め
BASE_VIEW_RATE = 0.0008 # 基礎露出を極限まで低減（情報の壁）
INITIAL_REVIVAL_PROB = random.uniform(0.005, 0.02) # 再燃は「奇跡」

# 動作変数
DECAY_PERCENT = INITIAL_DECAY_PERCENT
DECAY_MIN = 0.005
REVIVAL_PROB = INITIAL_REVIVAL_PROB
revival_count = 0
influence_boost_timer = 0 
current_impact_multiplier = 1.0
is_frenzy_mode = False

# --- 2. 初期化 ---
freshness = 1.0 
active_users = set()
initial_seed = random.randint(0, POPULATION-1)
active_users.add(initial_seed)

steps, new_posts_history, total_posts_history = [1], [1], [1]
revival_history = []

def get_status_bar(percent, width=20):
    filled = int(width * percent / 100)
    return "[" + "█" * filled + "░" * (width - filled) + "]"

print("\n" + "="*85)
print(f" 💀 トレンドシミュレーター：カオス＆格差版 開始 ".center(85, "="))
print(f" {'[初期運命]':<20} | 適合度:{MARKET_FIT:.2f} | 基礎威力:{IMPACT:.2f} ")
print(f" {'[市場環境]':<20} | 基礎露出:{BASE_VIEW_RATE:.4f} | 初期減衰:{INITIAL_DECAY_PERCENT:.1%} ")
print("="*85 + "\n")

# --- 3. メインループ ---
step = 1
while True:
    step += 1
    new_posts = 0
    
    # 【アルゴリズムの冷遇】直近の活動が少ないと、おすすめから完全に消える「死の谷」
    avg_activity = np.mean(new_posts_history[-5:]) if len(new_posts_history) >= 5 else new_posts_history[-1]
    visibility_penalty = 0.05 if avg_activity < 1.5 else (0.3 if avg_activity < 5 else 1.0)
    
    growth_factor = avg_activity * 0.02
    dynamic_view_rate = min(0.12, BASE_VIEW_RATE * (1 + growth_factor) * visibility_penalty)
    
    # インフルエンサー効果
    if influence_boost_timer > 0:
        influence_boost_timer -= 1
        active_impact = IMPACT * current_impact_multiplier
    else:
        current_impact_multiplier = 1.0
        active_impact = IMPACT
        is_frenzy_mode = False 

    # 拡散判定
    for i in range(POPULATION):
        if i not in active_users:
            if random.random() < (dynamic_view_rate * user_interests[i]):
                luck = random.uniform(-0.12, 0.12) # 運要素を拡大
                if (active_impact * freshness) + luck > user_thresholds[i]:
                    active_users.add(i)
                    new_posts += 1
    
    steps.append(step)
    new_posts_history.append(new_posts)
    total_posts_history.append(len(active_users))

    # --- 4. 再燃イベント（確率は低く、格差は大きく） ---
    revival_occurred = False
    if random.random() < REVIVAL_PROB:
        revival_count += 1
        roll = random.random()
        if is_frenzy_mode: roll += 0.15 # 確変

        if roll > 0.95: # 超強🔥 (SSR: 5%)
            p_label, n_prob, boost, mult, timer, d_cut = "超強🔥", 0.06, 0.85, 3.0, 20, 0.06
            BASE_VIEW_RATE = min(0.04, BASE_VIEW_RATE + 0.015)
            is_frenzy_mode = True
        elif roll > 0.70: # 強 (25%)
            p_label, n_prob, boost, mult, timer, d_cut = "強", 0.04, 0.5, 1.8, 10, 0.025
        elif roll > 0.40: # 並 (30%)
            p_label, n_prob, boost, mult, timer, d_cut = "並", 0.02, 0.25, 1.3, 5, 0.008
        else: # 弱 (40%)
            p_label, n_prob, boost, mult, timer, d_cut = "弱", 0.01, 0.05, 1.1, 2, 0.002
        
        freshness = min(1.0, freshness + boost)
        current_impact_multiplier = mult
        influence_boost_timer = timer
        REVIVAL_PROB = n_prob
        DECAY_PERCENT = max(DECAY_MIN, DECAY_PERCENT - d_cut)
        revival_history.append({"step": step, "power": p_label, "mult": mult, "reach": len(active_users)})
        revival_occurred = True

    # 自然減衰
    freshness *= (1.0 - DECAY_PERCENT)
    reach_p = (len(active_users) / POPULATION) * 100
    
    # ライブログ（10ステップごと、または再燃時のみ表示して高速化）
    if step % 10 == 0 or revival_occurred or step == 2:
        status = "🔥" if is_frenzy_mode else ("💀" if visibility_penalty < 1.0 else "  ")
        b_msg = f" [x{current_impact_multiplier:.1f}]" if current_impact_multiplier > 1.0 else f" [減衰:{DECAY_PERCENT:.1%}]"
        print(f"Step {step:4} {status} | {get_status_bar(reach_p)} {reach_p:5.1f}% | 新規:+{new_posts:3} | 合計:{len(active_users):4}人{b_msg}")
        if revival_occurred:
            print(f"  ┗━━ ★【再燃】: {p_label} (威力x{mult:.1f} / 飽きられにくさ改善!)")

    # --- 5. 終了判定（シビアな現実） ---
    if len(active_users) >= POPULATION:
        print("\n" + "👑 神話：5000人（全人口）到達！ ".center(85, "-"))
        break
    
    # 勢いが死んだら即終了。ブースト中でも鮮度が低すぎれば終了。
    if step > 20 and influence_boost_timer == 0:
        if freshness < 0.08 or (new_posts == 0 and step > 100): 
            print("\n" + f"⌛ 沈静化：最終到達 {len(active_users)}人 ({reach_p:.1f}%) / Step {step} で終了。 ".center(85, "-"))
            break
    if step > 5000: break

# --- 6. 最終結果グラフ ---
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(steps, new_posts_history, color='red', label='Momentum')
plt.title(f"Post Spike (Fit: {MARKET_FIT:.2f})")
plt.grid(True, alpha=0.2)

plt.subplot(1, 2, 2)
plt.plot(steps, total_posts_history, color='black', linewidth=2, label='Reach')
plt.axhline(y=POPULATION, color='red', linestyle='--', alpha=0.3)
plt.title(f"Final Reach: {len(active_users)} / 5000")
plt.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()