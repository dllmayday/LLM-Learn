import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(xmin, xmax, ymin, ymax, width, height, maxit=100, r=2):
    """
    计算指定矩形区域的曼德勃罗集发散时间矩阵
    参数：
        xmin, xmax: 实部范围
        ymin, ymax: 虚部范围
        width, height: 输出图像的宽度和高度（像素）
        maxit: 最大迭代次数
        r: 发散半径阈值
    返回：
        divtime: 形状为 (height, width) 的整型数组，表示首次发散时的迭代次数
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    A, B = np.meshgrid(x, y)
    C = A + B * 1j
    z = np.zeros_like(C)
    divtime = maxit * np.ones(z.shape, dtype=int)
    for i in range(maxit):
        z = z * z + C
        diverge = np.abs(z) > r
        div_now = diverge & (divtime == maxit)
        divtime[div_now] = i
        z[diverge] = r
    return divtime

# 全局变量，存储当前视图范围和图像对象
current_xmin, current_xmax = -2.5, 1.5
current_ymin, current_ymax = -1.5, 1.5
img_width, img_height = 800, 800  # 计算分辨率（越高越精细但慢）
max_iter = 200                     # 最大迭代次数，可随缩放增大而增大
img = None                         # 用于存储图像对象

def update_image():
    """重新计算并更新图像"""
    global img, current_xmin, current_xmax, current_ymin, current_ymax
    print(f"正在计算范围: x∈[{current_xmin:.6f}, {current_xmax:.6f}], y∈[{current_ymin:.6f}, {current_ymax:.6f}]")
    divtime = mandelbrot(current_xmin, current_xmax, current_ymin, current_ymax,
                         img_width, img_height, max_iter)
    if img is None:
        img = ax.imshow(divtime, cmap='hot', extent=[current_xmin, current_xmax, current_ymin, current_ymax])
    else:
        img.set_data(divtime)
        img.set_extent([current_xmin, current_xmax, current_ymin, current_ymax])
    ax.set_title(f"Mandelbrot Set (iter={max_iter})")
    plt.draw()

def on_click(event):
    """鼠标事件：左键放大，右键缩小"""
    global current_xmin, current_xmax, current_ymin, current_ymax, max_iter
    if event.inaxes != ax:
        return
    # 获取点击的坐标
    cx, cy = event.xdata, event.ydata
    if cx is None or cy is None:
        return
    # 当前区域宽度和高度
    width = current_xmax - current_xmin
    height = current_ymax - current_ymin
    if event.button == 1:        # 左键：放大2倍
        scale_factor = 0.5
        # 增加迭代次数以获得更精细的细节（可选）
        max_iter = min(max_iter * 2, 2000)   # 上限2000
    elif event.button == 3:      # 右键：缩小2倍
        scale_factor = 2.0
        max_iter = max(max_iter // 2, 50)    # 下限50
    else:
        return
    new_width = width * scale_factor
    new_height = height * scale_factor
    current_xmin = cx - new_width / 2
    current_xmax = cx + new_width / 2
    current_ymin = cy - new_height / 2
    current_ymax = cy + new_height / 2
    update_image()

def on_key(event):
    """键盘控制：按 r 重置视图"""
    global current_xmin, current_xmax, current_ymin, current_ymax, max_iter
    if event.key == 'r':
        current_xmin, current_xmax = -2.5, 1.5
        current_ymin, current_ymax = -1.5, 1.5
        max_iter = 200
        update_image()
    elif event.key == 'q':   # 按 q 退出
        plt.close()

# 创建图形和坐标轴
plt.ion()               # 打开交互模式
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlabel("Real")
ax.set_ylabel("Imaginary")
ax.set_title("Mandelbrot Set (Left click: zoom in, Right click: zoom out, R: reset)")

# 初始绘制
update_image()

# 绑定事件
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', on_key)

plt.ioff()             # 关闭交互模式，显示窗口
plt.show()