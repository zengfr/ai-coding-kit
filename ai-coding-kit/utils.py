"""Utility functions for AI Coding Kit"""
import sys
import platform
import subprocess
from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger():
    """Set up rich logger with统一格式"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, show_time=True, show_level=True, show_path=False)]
    )
    return logging.getLogger("ai-coding-kit")

logger = setup_logger()

def get_os():
    """获取当前操作系统"""
    os_name = platform.system().lower()
    if os_name in ["linux", "darwin", "windows"]:
        return os_name
    logger.warning(f"检测到未知操作系统: {os_name}，可能无法正常工作")
    return os_name

def check_command_exists(command):
    """检查命令是否存在"""
    try:
        # 对于Windows使用where，其他系统使用which
        check_cmd = "where" if get_os() == "windows" else "which"
        subprocess.run(
            [check_cmd, command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_command(command, shell=False, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            check=check,
            text=True
        )
        return result, True
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e.stderr}")
        return e, False