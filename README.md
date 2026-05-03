[The_Golden_Mean.py](c:/Users/rikiy/OneDrive/デスクトップ/Trends_theme/setting/The_Golden_Mean.py:1) は、ざっくり言うと **「トレンドやバズが人々に広がっていく様子をシミュレーションして、最後にグラフで可視化するコード」** です。



**全体像**

このコードは、5000人のユーザーがいる世界を作って、最初に1人だけがトレンドに反応します。そこからステップごとに、まだ反応していない人たちがそのトレンドを見るかどうか、興味を持つかどうかをランダムに判定して、どれくらい拡散したかを追跡します。

最後に、次の2つのグラフを表示します。

- 各ステップで新しく反応した人数
- 累計で何人まで広がったか

**読み込み部分**

```python
import random
import matplotlib.pyplot as plt
import numpy as np
```

ここでは3つのライブラリを使っています。

`random` はランダムな数値を作るため。  
`numpy` は大量のユーザーデータを作るため。  
`matplotlib.pyplot` は最後にグラフを描くためです。

**基本パラメータ**

```python
POPULATION = 5000
IMPACT = random.uniform(0.70, 0.92)
THRESHOLD_AVG = random.uniform(0.35, 0.45)
```

`POPULATION` はユーザー数です。ここでは5000人。

`IMPACT` はトレンド自体の強さです。0.70から0.92の間でランダムに決まります。数字が大きいほど、人に刺さりやすいトレンドになります。

`THRESHOLD_AVG` は、人々が反応するための平均的なハードルです。低いほど反応しやすく、高いほど反応しにくいです。

```python
INITIAL_DECAY_PERCENT = random.uniform(0.09, 0.12)
DECAY_PERCENT = INITIAL_DECAY_PERCENT
DECAY_MIN_BASE = 0.035
```

これはトレンドの鮮度が毎ステップどれくらい落ちるかを決めています。

`freshness` という値が後で出てきますが、これは「今どれくらい新鮮な話題か」です。時間が経つほど下がっていきます。

```python
BASE_VIEW_RATE = 0.004
REVIVAL_PROB = random.uniform(0.04, 0.07)
revival_success_count = 0
```

`BASE_VIEW_RATE` は、ユーザーがそのトレンドを目にする基本確率です。  
`REVIVAL_PROB` は、再燃イベントが起きる確率です。  
`revival_success_count` は、再燃が成功した回数です。

つまりこのコードでは、トレンドはただ衰退するだけでなく、たまに「再燃」して盛り返す可能性があります。

**ユーザーの初期化**

```python
user_thresholds = np.sort(np.random.normal(THRESHOLD_AVG, 0.15, POPULATION))
user_interests = np.random.uniform(0.5, 2.0, POPULATION)
active_users = set()
active_users.add(random.randint(0, POPULATION-1))
```

ここがかなり大事です。

`user_thresholds` は、各ユーザーが反応するために必要なハードルです。  
たとえば、ある人は流行に敏感なので低いハードルで反応します。別の人は慎重なので、高いハードルが必要です。

`np.random.normal(...)` を使っているので、平均値の周辺に多くの人が集まり、一部に反応しやすい人・反応しにくい人が出ます。

`user_interests` は、各ユーザーの興味の強さです。0.5から2.0の間で決まります。  
2.0に近い人ほど、その話題を見やすい、または関心を持ちやすい人です。

`active_users` は、すでにトレンドに反応したユーザーの集合です。  
最初にランダムな1人を追加して、そこから拡散が始まります。

**履歴データ**

```python
steps, new_posts_history, total_posts_history = [1], [1], [1]
freshness = 1.0
max_momentum = 0
revival_logs = []
```

`steps` は時間の流れです。  
`new_posts_history` は各ステップで新しく反応した人数。  
`total_posts_history` は累計の反応人数。

`freshness = 1.0` は、最初はトレンドの鮮度が100%という意味です。  
`max_momentum` は、1ステップで最も多く増えた人数を記録します。  
`revival_logs` は、再燃イベントの記録用です。

**進捗バー関数**

```python
def get_status_bar(percent, width=20):
    filled = int(width * percent / 100)
    return "[" + ... + "]"
```

これは、拡散率をコンソール上でバー表示するための関数です。

たとえば `percent = 50` なら、20マス中10マスが埋まるような表示を作る意図です。

ただし現在の31行目は文字化けで壊れているため、この関数は修正が必要です。本来はおそらくこんな形です。

```python
return "[" + "#" * filled + "-" * (width - filled) + "]"
```

**メインループ**

```python
step = 1
while True:
    step += 1
    new_posts = 0
    current_reach_p = (len(active_users) / POPULATION) * 100
```

ここからシミュレーション本体です。

`while True` なので、終了条件に達するまでずっと繰り返します。

`current_reach_p` は、現在どれくらいの割合の人に広がったかです。  
たとえば5000人中1000人なら20%です。

**広がりにくさ resistance**

```python
resistance = 1.0
if current_reach_p > 20: resistance += (current_reach_p - 20) * 0.008
if current_reach_p > 60: resistance += (current_reach_p - 60) * 0.02
```

これは「広がれば広がるほど、伸びにくくなる」仕組みです。

最初は新鮮で広がりやすいですが、20%を超えると少し抵抗が増えます。  
60%を超えるとさらに抵抗が強くなります。

現実のトレンドでも、最初は勢いよく広がっても、後半になると「もう知ってる人が多い」「興味ない人だけが残る」ので伸びにくくなります。それを再現しています。

**鮮度の減衰**

```python
decay_min = max(0.025, DECAY_MIN_BASE - (revival_success_count * 0.003))
current_decay = min(0.35, DECAY_PERCENT * resistance)
```

`current_decay` は、このステップでどれだけ鮮度が落ちるかです。

`resistance` が大きいほど、鮮度の落ち方も大きくなります。  
ただし `min(0.35, ...)` によって、最大でも35%までに制限されています。

`decay_min` は、再燃が成功するたびに下がります。つまり、再燃に成功するとトレンドが少し長持ちする設計です。

**同調圧力 peer_pressure**

```python
peer_pressure = 1.0
if current_reach_p > 75:
    peer_pressure = 1.0 + (current_reach_p - 75) * 0.12
```

これはかなり面白い部分です。

75%を超えるほど広がると、「みんな見てるから自分も反応する」という効果が強くなります。  
つまり、ある程度まで行くと逆に最後の人たちも巻き込まれやすくなります。

**直前の勢いによる視聴率アップ**

```python
prev_momentum = new_posts_history[-1] * 0.01
dynamic_view_rate = min(0.09, BASE_VIEW_RATE * (1 + prev_momentum))
```

直前のステップで新しく反応した人が多いほど、次のステップでさらに見られやすくなります。

これはSNSのアルゴリズムっぽい動きです。  
勢いがある投稿はおすすめに乗りやすくなり、さらに見られやすくなる、という仕組みですね。

ただし `min(0.09, ...)` によって、最大9%までに制限されています。

**ユーザーごとの反応判定**

```python
for i in range(POPULATION):
    if i not in active_users:
        if random.random() < (dynamic_view_rate * user_interests[i]):
            luck = random.uniform(-0.05, 0.05)
            effective_impact = IMPACT * max(0.25, (1.0 - (current_reach_p / 350))) * peer_pressure
            
            if (effective_impact * freshness) + luck > user_thresholds[i]:
                active_users.add(i)
                new_posts += 1
```

ここがシミュレーションの中心です。

まだ反応していない全ユーザーを1人ずつ見て、まず「そのトレンドを目にするか」を判定します。

```python
random.random() < (dynamic_view_rate * user_interests[i])
```

興味が強いユーザーほど見やすく、トレンドの勢いが強いほど見やすいです。

次に、実際に反応するかを判定します。

```python
(effective_impact * freshness) + luck > user_thresholds[i]
```

意味としては、

```text
トレンドの強さ × 鮮度 + 運 > その人の反応ハードル
```

です。

この条件を超えたら、そのユーザーは `active_users` に追加されます。  
そして `new_posts` が1増えます。

**再燃イベント**

```python
revival_occurred = False
if random.random() < REVIVAL_PROB:
    quality = random.uniform(0.05, 0.6)
    freshness = min(1.0, freshness + max(0.2, quality))
```

一定確率で再燃イベントが起きます。

これはたとえば、

- 有名人が取り上げた
- 別の文脈で話題になった
- 二次創作やミーム化した
- ニュースに再掲載された

みたいな出来事を表していると思われます。

`quality` が高いほど、再燃の質が高いです。  
再燃すると `freshness` が回復します。ただし最大は1.0です。

```python
if quality > 0.15:
    revival_success_count += 1
    DECAY_PERCENT = max(decay_min, DECAY_PERCENT - 0.012)
    BASE_VIEW_RATE = min(0.018, BASE_VIEW_RATE + 0.0018)
```

再燃の質がある程度高い場合、成功扱いになります。

成功すると、

- `revival_success_count` が増える
- `DECAY_PERCENT` が下がる
- `BASE_VIEW_RATE` が上がる

つまり、トレンドが長持ちしやすくなり、見られやすくなります。

**鮮度を落とす**

```python
freshness *= (1.0 - current_decay)
```

各ステップの最後に鮮度が落ちます。

たとえば `current_decay = 0.1` なら、

```text
freshness = freshness × 0.9
```

になります。

これによって、時間が経つほど反応されにくくなります。

**途中経過の表示**

```python
if step % 10 == 0 or revival_occurred:
    print(...)
```

10ステップごと、または再燃イベントが起きたときに、現在の拡散率や新規反応数を表示します。

ただし表示文字列が文字化けしているため、今は読みにくい状態です。

**終了条件**

```python
if len(active_users) >= POPULATION:
    reason = ...
    break
```

全員に広がったら終了です。

```python
if step > 20 and (freshness < 0.025 or (new_posts == 0 and step > 140)):
    reason = ...
    break
```

20ステップを超えたあと、鮮度がほぼなくなった場合、または140ステップ以降で新規反応が0なら終了です。  
つまり「もう流行が終わった」と判断します。

```python
if step > 2500:
    reason = ...
    break
```

2500ステップを超えたら強制終了します。無限ループ対策です。

**最終レポート**

```python
final_count = len(active_users)
```

最後に、何人まで広がったかを計算します。

そのあと、

```python
if current_reach_p < 10:
    res = ...
elif current_reach_p < 35:
    res = ...
elif current_reach_p < 65:
    res = ...
elif current_reach_p < 90:
    res = ...
else:
    res = ...
```

拡散率によって結果を分類しています。

おそらく意図としては、

- 10%未満: 不発
- 35%未満: 局所流行
- 65%未満: プチバズ
- 90%未満: ヒット
- 90%以上: 社会現象

のような分類だと思います。

**グラフ描画**

```python
plt.figure(figsize=(14, 6))
```

横長のグラフ画面を作ります。

左側のグラフはこちらです。

```python
plt.subplot(1, 2, 1)
plt.plot(steps, new_posts_history, color='orange', label='New Users per Step')
plt.fill_between(steps, new_posts_history, color='orange', alpha=0.2)
```

各ステップで新しく反応した人数を表示します。  
これは「勢い」のグラフです。

右側のグラフはこちらです。

```python
plt.subplot(1, 2, 2)
plt.plot(steps, total_posts_history, color='dodgerblue', linewidth=2.5, label='Total Reach')
```

累計で何人まで広がったかを表示します。  
これは「最終的な到達人数」のグラフです。

```python
plt.axhline(y=POPULATION * 0.9, ...)
plt.axhline(y=POPULATION * 0.65, ...)
plt.axhline(y=POPULATION * 0.35, ...)
```

ここでは基準線を引いています。

- 90%: Social Phenomenon
- 65%: Major Hit
- 35%: Petit Buzz

つまり、どのレベルの流行になったかを視覚的に見やすくしています。

**このコードの本質**

このコードは、単なるランダム拡散ではなく、かなりそれっぽい要素を入れています。

- 人によって反応しやすさが違う
- 人によって興味の強さが違う
- トレンドには鮮度がある
- 時間が経つと飽きられる
- 勢いがあるとさらに見られやすい
- 広まりすぎると伸びにくくなる
- でも75%を超えると同調圧力で再加速する
- たまに再燃イベントが起きる

なので、SNS上のバズやトレンド拡散を、簡易的な数理モデルとして表現したコードです。

一番大事な式はここです。

```python
if (effective_impact * freshness) + luck > user_thresholds[i]:
```

これは、

```text
トレンドの魅力 × 今の鮮度 + 偶然性 > その人が反応するハードル
```

という意味です。

この条件を満たした人が、トレンドに参加していきます。

