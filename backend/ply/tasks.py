from celery import shared_task
import psutil
import subprocess


@shared_task
def run_gaussian():
    # 使用 psutil 检查 gaussian.py 是否正在运行
    gaussian_running = False
    for process in psutil.process_iter(['name', 'cmdline']):
        # 检查进程名字或命令行中是否含有 'gaussian.py'
        if process.info['cmdline'] and 'gaussian.py' in process.info['cmdline']:
            gaussian_running = True
            break

    if not gaussian_running:
        print("启动 gaussian.py...")
        # 在这里替换为实际启动你的脚本的命令
        subprocess.Popen(['python', 'gaussian.py'])
    else:
        print("gaussian.py 已经在运行.")