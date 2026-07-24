#!/usr/bin/env python3
"""
自动点击工具
更新需求：
1. 删除【进行至第x步】文字，只保留累计耗时
2. 全局单条原地刷新渐变进度条（红→黄→绿）
3. 大循环之间空两行分隔，方便阅读
4. 持续优化运行速度
5. 布局：进度条行 + 纯累计耗时信息行
"""
import time
import pyautogui
import sys

# 渐变色彩生成 红→黄→绿
def get_grad_block(pos: int, fill_len: int, bar_total: int):
    if pos >= fill_len:
        return "□"
    ratio = pos / bar_total
    if ratio < 0.5:
        r = 255
        g = int(ratio * 2 * 255)
        b = 0
    else:
        ratio2 = (ratio - 0.5) * 2
        r = int(255 - ratio2 * 255)
        g = 255
        b = 0
    return f"\033[38;2;{r};{g};{b}m■\033[0m"

def main():
    # 输入循环次数
    while True:
        try:
            input_str = input("请输入需要执行的大循环次数（正整数）：")
            total_big_cycles = int(input_str)
            if total_big_cycles > 0:
                break
            print("数值必须大于0，请重新输入！")
        except ValueError:
            print("输入格式错误，请输入数字！")

    # 延时参数
    normal_delay = 0.1
    step_input_delay = 0.3
    loop_end_delay = 0.4
    sub_per_big = 10
    total_sub = total_big_cycles * sub_per_big
    bar_length = 60

    # 预估耗时
    single_sub_sleep = 8 * normal_delay + step_input_delay + loop_end_delay
    single_sub_estimate = single_sub_sleep + 0.2
    estimate_seconds = total_sub * single_sub_estimate
    estimate_min = estimate_seconds / 60

    print(f"\n====任务预估信息====")
    print(f"大循环数量：{total_big_cycles} 个")
    print(f"小轮总数量：{total_sub} 个")
    print(f"预估总耗时：{estimate_seconds:.1f} 秒 ≈ {estimate_min:.2f} 分钟")
    confirm = input("\n确认开始执行？输入 y 开始，其他任意字符退出：").strip().lower()
    if confirm != "y":
        print("已取消任务，程序退出")
        return

    start_time = time.time()
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0
    input_text = "$CAMRYHOOD"
    finished_sub = 0

    dynamic_coords = [
        (1750, 388),
        (1760, 388),
        (1771, 388),
        (1783, 388),
        (1793, 388),
        (1804, 388),
        (1816, 388),
        (1827, 388),
        (1837, 388),
        (1848, 388)
    ]

    step_text_template = """  第一步：点击坐标 1745,161，功能：确定选中钱包。
  第二步：点击坐标 1577,218，功能：进入修改项。
  第三步：点击坐标 1577,218，功能：确认进入。
  第四步：点击动态坐标（共100个），功能：寻找真实的编辑按钮。
  第五步：点击坐标 1857,559，功能：删除名称。
  第六步：输入名称，功能：输入 $CAMRYHOOD。
  第七步：点击坐标 1804,656，功能：点击确定。
  第八步：点击坐标 1644,656，功能：点击取消。
  第九步：点击坐标 1644,655，功能：二次点击取消。
  第十步：点击坐标 1577,215，功能：点击后退。"""

    print("\n====任务开始====")
    for big_loop in range(1, total_big_cycles + 1):
        # 循环之间空两行
        if big_loop > 1:
            print("\n\n")
        print(f"【循环：第{big_loop}次/共{total_big_cycles}次】")
        print(step_text_template)

        for sub_idx, (dyn_x, dyn_y) in enumerate(dynamic_coords, 1):
            steps_info = [
                {"xy": (1745, 161)},
                {"xy": (1577, 218)},
                {"xy": (1577, 218)},
                {"xy": (dyn_x, dyn_y)},
                {"xy": (1857, 559)},
                {"xy": None},
                {"xy": (1804, 656)},
                {"xy": (1644, 656)},
                {"xy": (1644, 655)},
                {"xy": (1577, 215)}
            ]

            for step_num, item in enumerate(steps_info, 1):
                x, y = item["xy"] if item["xy"] else (None, None)
                try:
                    progress = finished_sub / total_sub
                    fill_count = int(bar_length * progress)
                    bar_list = [get_grad_block(i, fill_count, bar_length) for i in range(bar_length)]
                    mark_pos = min(fill_count, bar_length - 1)
                    bar_list[mark_pos] = str(step_num)
                    bar_str = "".join(bar_list)
                    current_elapsed = time.time() - start_time

                    # 移除“进行至第x步”，仅保留累计耗时
                    sys.stdout.write(f"\r{bar_str} {progress:.1%}\n累计耗时:{current_elapsed:.2f}s\033[A")
                    sys.stdout.flush()

                    if x is not None:
                        pyautogui.moveTo(x, y, duration=0.06)
                        pyautogui.click(x=x, y=y, clicks=1, interval=0.0)
                        if step_num == 2:
                            nx, ny = steps_info[2]["xy"]
                            pyautogui.moveTo(nx, ny, duration=0.06)
                    else:
                        pyautogui.write(input_text)
                        pyautogui.press('enter')

                    if step_num < 10:
                        wait = step_input_delay if step_num == 6 else normal_delay
                        time.sleep(wait)
                except Exception as e:
                    print(f"\n>>>异常：{e}")
                    time.sleep(3)

            time.sleep(loop_end_delay)
            finished_sub += 1

    # 任务完成最终进度条
    progress = finished_sub / total_sub
    fill_count = int(bar_length * progress)
    bar_list = [get_grad_block(i, fill_count, bar_length) for i in range(bar_length)]
    bar_str = "".join(bar_list)
    total_cost = time.time() - start_time
    sys.stdout.write(f"\r{bar_str} {progress:.1%}\n✅ 全部任务结束！总耗时：{total_cost:.2f} 秒\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
