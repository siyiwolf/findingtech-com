#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt

# 加载数据
with open('span-data.json') as f:
    data = json.load(f)

products = data['products']

# 提取坐标和颜色
def get_quadrant(m, c):
    mid = 50
    if m >= mid and c >= mid: return '#4CAF50'  # Q1 绿
    if m >= mid and c < mid: return '#FFC107'   # Q2 黄
    if m < mid and c < mid: return '#F44336'   # Q3 红
    return '#2196F3'                            # Q4 蓝

xs = [p['market'] for p in products]
ys = [p['comp'] for p in products]
colors = [get_quadrant(p['market'], p['comp']) for p in products]
labels = [f"{p['id']}: {p['name']}" for p in products]

# 图表
plt.figure(figsize=(12,8))
plt.scatter(xs, ys, c=colors, s=60, alpha=0.8, edgecolors='white', linewidth=0.5)

# 象限分隔线
plt.axhline(50, color='gray', linestyle='--', linewidth=1)
plt.axvline(50, color='gray', linestyle='--', linewidth=1)

# 标签（仅标记前10个高价值点，避免重叠）
top10 = sorted(products, key=lambda p: p['market']+p['comp'], reverse=True)[:10]
for p in top10:
    plt.text(p['market']+1, p['comp']+1, f"{p['id']}", fontsize=8, color='black', weight='bold')

plt.title('SPAN Analysis: 100 Outdoor Smart Products', fontsize=16, pad=20)
plt.xlabel('Market Attractiveness (0-100)', fontsize=12)
plt.ylabel('Competitive Strength (0-100)', fontsize=12)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.3)

# 保存PNG
plt.savefig('span-chart.png', dpi=150, bbox_inches='tight')
print("✅ span-chart.png generated")