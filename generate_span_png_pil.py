#!/usr/bin/env python3
import json
from PIL import Image, ImageDraw

# 画布设置
W, H = 1000, 700
margin = 60
plot_w = W - 2*margin
plot_h = H - 2*margin

img = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(img)

# 加载数据
with open('span-data.json') as f:
    data = json.load(f)
products = data['products']

def to_coord(market, comp):
    x = margin + (market/100)*plot_w
    y = margin + plot_h - (comp/100)*plot_h
    return x, y

# 绘制网格和轴线
draw.line([margin, margin, margin, H-margin], fill='black', width=2)  # Y轴
draw.line([margin, H-margin, W-margin, H-margin], fill='black', width=2)  # X轴
# 刻度
for i in range(0, 101, 25):
    x = margin + (i/100)*plot_w
    y = H-margin + 20
    draw.text((x-10, y), str(i), fill='black')
    # 网格线
    if i>0:
        draw.line([x, margin, x, H-margin], fill='#eee', width=1)
        y_line = margin + plot_h - (i/100)*plot_h
        draw.line([margin, y_line, W-margin, y_line], fill='#eee', width=1)

# 绘制分隔线
mid_x = margin + 0.5*plot_w
mid_y = margin + 0.5*plot_h
draw.line([mid_x, margin, mid_x, H-margin], fill='gray', width=2)
draw.line([margin, mid_y, W-margin, mid_y], fill='gray', width=2)

# 象限标签
def get_quadrant(m, c):
    mid = 50
    if m >= mid and c >= mid: return '#4CAF50'
    if m >= mid and c < mid: return '#FFC107'
    if m < mid and c < mid: return '#F44336'
    return '#2196F3'

quadrants = [
    (65, 65, '#4CAF50', 'Q1:优先执行'),
    (85, 85, '#FFC107', 'Q2:需投资'),
    (15, 15, '#F44336', 'Q3:避免'),
    (15, 85, '#2196F3', 'Q4:利基/出口')
]
for qx, qy, col, txt in quadrants:
    draw.text((margin + (qx/100)*plot_w - 30, margin + plot_h - (qy/100)*plot_h - 20), txt, fill=col)

# 绘制数据点
for p in products:
    x, y = to_coord(p['market'], p['comp'])
    color = get_quadrant(p['market'], p['comp'])
    draw.ellipse([x-4, y-4, x+4, y+4], fill=color, outline='white')

# 标题
draw.text((W//2 - 200, 20), 'SPAN Analysis: 100 Outdoor Smart Products', fill='black', font=None)

img.save('span-chart.png')
print("✅ span-chart.png generated")