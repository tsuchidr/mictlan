import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


# コスト関数を定義します。
def c_e1(k):
    return 3 + 3 * k


def c_e2(k):
    return 19 + k


def c_e3(k):
    return 19 + k


def c_e4(k):
    return 3 + 3 * k


def c_e5(k):
    return 6 + k


# 各車両の効用関数を定義します。
def U_i(a_i, a):
    roads = set(a_i)
    return 45 - sum(eval(f"c_{r}({a.count(r)})") for r in roads)


# 経路を定義します。
paths = {
    'p1': ['e1', 'e3'],
    'p2': ['e2', 'e4'],
    'p3': ['e1', 'e4', 'e5']
}

# 温度パラメータを定義します。
temperature = 1.0

# 初期行動プロファイルをランダムに選択します。
num_players = 4
actions = list(paths.keys())
current_profile = [random.choice(actions) for _ in range(num_players)]

# 各反復におけるプレイヤーの選択を保存するためのリスト
profiles_history = [current_profile.copy()]

# Log-Linear Learningを実行します。
num_iterations = 150
for _ in range(num_iterations):
    # ランダムにプレイヤーを選択します。
    player = random.randint(0, num_players - 1)

    # 現在の行動を保持します。
    current_action = current_profile[player]

    # 他のすべての行動に対する効用を計算します。
    utilities = []
    for action in actions:
        current_profile[player] = action
        utility = U_i(paths[action], [road for p in current_profile for road in paths[p]])
        utilities.append(utility)

    # 効用に基づいて確率を計算します。
    exp_utilities = np.exp(np.array(utilities) / temperature)
    probabilities = exp_utilities / np.sum(exp_utilities)

    # 新しい行動を確率的に選択します。
    new_action = np.random.choice(actions, p=probabilities)

    # プロファイルを更新します。
    current_profile[player] = new_action
    profiles_history.append(current_profile.copy())

# 最終的な行動プロファイルと効用を出力します。
print("Final profile:", current_profile)
final_utilities = [U_i(paths[action], [road for p in current_profile for road in paths[p]]) for action in
                   current_profile]
print("Final utilities:", final_utilities)

# プロファイル履歴をデータフレームに変換して保存します。
df_profiles = pd.DataFrame(profiles_history, columns=[f'Player_{i}' for i in range(1, num_players + 1)])
df_profiles.to_csv('profiles_history.csv', index=False)

# 各プレイヤーの各経路の選択確率を計算します。
path_choices = {player: {path: [] for path in paths.keys()} for player in df_profiles.columns}
for _, profile in df_profiles.iterrows():
    for player, path in profile.items():
        for p in paths.keys():
            path_choices[player][p].append(1 if path == p else 0)

# 選択確率の推移を計算します。
rolling_window = 100
path_probabilities = {player: {path: [] for path in paths.keys()} for player in df_profiles.columns}
for player in df_profiles.columns:
    for path in paths.keys():
        path_probabilities[player][path] = pd.Series(path_choices[player][path]).rolling(window=rolling_window).mean()

# プロットを作成します。
fig, axes = plt.subplots(num_players, 1, figsize=(10, 20), sharex=True)
for i, player in enumerate(df_profiles.columns):
    ax = axes[i]
    for path in paths.keys():
        ax.plot(path_probabilities[player][path], label=path)
    ax.set_title(f'Player {i + 1}')
    ax.set_ylabel('Probability')
    ax.legend()
plt.xlabel('Iteration')
plt.show()

# 最後の100回の平均プロファイルを出力します。
average_profile = df_profiles.iloc[-100:].mode().iloc[0]
print("Average profile in the last 100 iterations:", average_profile.tolist())
