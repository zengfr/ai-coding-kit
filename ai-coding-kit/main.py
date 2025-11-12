"""AI Coding Kit 主程序入口"""
from .utils import logger, console
from .installer import ToolInstaller
from rich import print as rprint
import sys

def main():
    """主函数"""
    rprint("[bold blue]=== AI Coding Kit ===")
    logger.info("欢迎使用AI工具集成套件")
    logger.info("本工具将帮助您安装指定的AI开发工具")

    try:
        installer = ToolInstaller()
        installer.choose_and_install()
        rprint("\n[bold green]操作完成!")
    except Exception as e:
        logger.error(f"发生错误: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()