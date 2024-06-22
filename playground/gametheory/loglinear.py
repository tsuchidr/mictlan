import numpy as np
import pandas as pd
from itertools import product


# コスト関数を定義します。
# c_e1(k): 道路e1のコスト関数。通行車両数kに応じてコストが増加します。
def c_e1(k):
    return 3 + 3 * k


# c_e2(k): 道路e2のコスト関数。通行車両数kに応じてコストが増加します。
def c_e2(k):
    return 19 + k


# c_e3(k): 道路e3のコスト関数。通行車両数kに応じてコストが増加します。
def c_e3(k):
    return 19 + k


# c_e4(k): 道路e4のコスト関数。通行車両数kに応じてコストが増加します。
def c_e4(k):
    return 3 + 3 * k


# c_e5(k): 道路e5のコスト関数。通行車両数kに応じてコストが増加します。
def c_e5(k):
    return 6 + k


# 目的関数を定義します。
def W_r(r, k):
    # W_r(r, k): 道路rの目的関数。特定の道路rにおける車両数kの時の評価値を計算します。
    # 'e1', 'e4', 'e5'の場合と'e2', 'e3'の場合で異なる計算を行います。
    if r in ['e1', 'e4', 'e5']:
        return k * (15 - eval(f"c_{r}({k})"))
    elif r in ['e2', 'e3']:
        return k * (30 - eval(f"c_{r}({k})"))


# 各車両の効用関数を定義します。
def U_i(a_i, a):
    # U_i(a_i, a): 車両iの効用関数。車両iの選択した経路a_iと全車両の経路aに基づいて効用を計算します。
    # 具体的には、特定の車両が選んだ経路に含まれる各道路のコストの合計を引くことで効用を計算します。
    roads = set(a_i)
    return 45 - sum(eval(f"c_{r}({a.count(r)})") for r in roads)


# グローバル目的関数を定義します。
def W(a):
    # W(a): 全体の目的関数。全車両の経路aに基づいて全体の評価値を計算します。
    # すべての道路について、その道路を通る車両数に対する目的関数の合計を求めます。
    return sum(W_r(r, a.count(r)) for r in set(a))


# ポテンシャル関数を定義します。
def phi(a):
    # phi(a): ポテンシャル関数。全車両の経路aに基づいてポテンシャル値を計算します。
    # 具体的には、すべての道路について、その道路を通る車両数に応じたコストの合計を負の値として計算します。
    return -sum(sum(eval(f"c_{r}({k})") for k in range(1, a.count(r) + 1)) for r in set(a))


# 経路を定義します。
# paths: 経路の辞書。各経路p1, p2, p3は特定の道路のリストとして定義されています。
paths = {
    'p1': ['e1', 'e3'],
    'p2': ['e2', 'e4'],
    'p3': ['e1', 'e4', 'e5']
}

# すべての可能な行動プロファイルを作成します。
action_profiles = list(product(paths.keys(), repeat=4))
# action_profiles: すべての可能な行動プロファイルのリスト。4つの車両がそれぞれp1, p2, p3のいずれかの経路を選択する全組み合わせを生成します。

# ナッシュ均衡とWを最大化するプロファイルを探します。
nash_equilibria = []
max_W = -np.inf
optimal_profile = None

# すべての行動プロファイルについてループします。
for profile in action_profiles:
    # 現在の行動プロファイルに対する各車両の効用を計算します。
    current_U = [U_i(paths[profile[i]], [road for p in profile for road in paths[p]]) for i in range(4)]
    # 各行動プロファイルについてナッシュ均衡をチェックします
    is_nash_equilibrium = True
    for i in range(4):  # 各車両iについて
        # 車両iが現在の経路profile[i]を選択した場合の効用を計算します
        current_utility = U_i(paths[profile[i]], [road for profile_path in profile for road in paths[profile_path]])

        for p in paths.keys():  # すべての経路pについて
            # 車両iが経路pを選択した場合の効用を計算します
            potential_utility = U_i(paths[p], [road for profile_path in profile for road in paths[profile_path]])
            # 現在の経路が他の経路よりも効用が低い場合はナッシュ均衡ではない
            if current_utility < potential_utility:
                is_nash_equilibrium = False
                break
        if not is_nash_equilibrium:
            break

    # ナッシュ均衡であれば、そのプロファイルをナッシュ均衡リストに追加します
    if is_nash_equilibrium:
        nash_equilibria.append(profile)

    # 現在の行動プロファイルに対する全体の目的関数Wを計算します。
    current_W = W([road for p in profile for road in paths[p]])

    # 最大のWを持つプロファイルを更新します。
    if current_W > max_W:
        max_W = current_W
        optimal_profile = profile

# ナッシュ均衡、最適なプロファイル、および最大のWの値を出力します。
for i in nash_equilibria:
    print(i)

print(len(nash_equilibria))
print(optimal_profile, max_W)

# Number of players
players = 4
strategies = list(paths.keys())


# Function to calculate payoffs
def calculate_payoffs(profile):
    return [U_i(paths[profile[i]], [road for p in profile for road in paths[p]]) for i in range(players)]


# Generate all action profiles
action_profiles = list(product(strategies, repeat=players))

# Calculate payoffs for each action profile
payoffs = [calculate_payoffs(profile) for profile in action_profiles]

# Create dataframe
columns = [f'Player {i + 1}' for i in range(players)] + [f'Payoff {i + 1}' for i in range(players)]
data = [list(profile) + payoff for profile, payoff in zip(action_profiles, payoffs)]
df = pd.DataFrame(data, columns=columns)

# Display the dataframe
df.head()
