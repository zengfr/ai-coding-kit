"""安装工具类"""
from .utils import logger, check_command_exists, run_command, get_os, console
from rich.prompt import Prompt
from rich.progress import Progress

class ToolInstaller:
    """工具安装器"""
    SUPPORTED_TOOLS = {
        "openspec": {
            "description": "Open specification tool from Fission AI",
            "dependencies": ["npm"],
            "install_command": ["npm", "install", "-g", "@fission-ai/openspec@latest"]
        },
        "spec-kit": {
            "description": "Specification kit from GitHub",
            "dependencies": ["uv", "git"],
            "install_command": ["uv", "tool", "install", "specify-cli", "--from", "git+https://github.com/github/spec-kit.git"]
        }
    }

    def __init__(self):
        self.os = get_os()

    def check_dependencies(self, tool_name):
        """检查单个工具依赖"""
        if tool_name not in self.SUPPORTED_TOOLS:
            logger.error(f"不支持的工具: {tool_name}")
            return False

        tool_info = self.SUPPORTED_TOOLS[tool_name]
        missing_deps = []

        for dep in tool_info["dependencies"]:
            if not check_command_exists(dep):
                missing_deps.append(dep)

        if missing_deps:
            logger.warning(f"检测到缺失依赖: {', '.join(missing_deps)}")
            install = Prompt.ask(f"是否要安装这些依赖?", choices=["y", "n"], default="y")
            if install.lower() == "y":
                return self.install_dependencies(missing_deps)
            else:
                logger.error("依赖缺失，无法继续安装工具")
                return False
        return True

    def install_dependencies(self, dependencies):
        """安装依赖"""
        with Progress() as progress:
            task = progress.add_task("[cyan]安装依赖...", total=len(dependencies))
            
            for dep in dependencies:
                progress.update(task, description=f"[cyan]安装 {dep}...")
                
                if dep == "npm":
                    success = self._install_npm()
                elif dep == "uv":
                    success = self._install_uv()
                elif dep == "git":
                    success = self._install_git()
                else:
                    logger.error(f"不支持自动安装依赖: {dep}")
                    success = False

                if not success:
                    logger.error(f"依赖 {dep} 安装失败")
                    return False
                
                progress.update(task, advance=1)
        
        return True

    def _install_npm(self):
        """安装npm (Node.js)"""
        logger.info("开始安装Node.js (包含npm)")
        
        if self.os == "windows":
            logger.info("请手动安装Node.js: https://nodejs.org/")
            return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"
        elif self.os == "darwin":  # macOS
            if check_command_exists("brew"):
                logger.info("使用Homebrew安装Node.js")
                result, success = run_command(["brew", "install", "node"])
                return success
            else:
                logger.info("请手动安装Node.js: https://nodejs.org/ 或先安装Homebrew: https://brew.sh/")
                return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"
        else:  # Linux
            if check_command_exists("apt"):
                logger.info("使用apt安装Node.js")
                result, success = run_command(["sudo", "apt", "update"])
                if not success:
                    return False
                result, success = run_command(["sudo", "apt", "install", "-y", "nodejs", "npm"])
                return success
            elif check_command_exists("yum"):
                logger.info("使用yum安装Node.js")
                result, success = run_command(["sudo", "yum", "install", "-y", "nodejs", "npm"])
                return success
            else:
                logger.info("请手动安装Node.js: https://nodejs.org/")
                return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"

    def _install_uv(self):
        """安装uv"""
        logger.info("开始安装uv")
        
        if self.os == "windows":
            result, success = run_command(["powershell", "-Command", "iwr https://astral.sh/uv/install.ps1 | iex"], shell=True)
            return success
        else:
            result, success = run_command(["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"], shell=True)
            return success

    def _install_git(self):
        """安装git"""
        logger.info("开始安装git")
        
        if self.os == "windows":
            logger.info("请手动安装Git: https://git-scm.com/download/win")
            return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"
        elif self.os == "darwin":  # macOS
            if check_command_exists("brew"):
                logger.info("使用Homebrew安装Git")
                result, success = run_command(["brew", "install", "git"])
                return success
            else:
                logger.info("Git通常预装在macOS上，或者请手动安装: https://git-scm.com/")
                return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"
        else:  # Linux
            if check_command_exists("apt"):
                logger.info("使用apt安装Git")
                result, success = run_command(["sudo", "apt", "update"])
                if not success:
                    return False
                result, success = run_command(["sudo", "apt", "install", "-y", "git"])
                return success
            elif check_command_exists("yum"):
                logger.info("使用yum安装Git")
                result, success = run_command(["sudo", "yum", "install", "-y", "git"])
                return success
            else:
                logger.info("请手动安装Git: https://git-scm.com/")
                return Prompt.ask("安装完成后请输入 'y'", choices=["y", "n"], default="n") == "y"

    def install_tool(self, tool_name):
        """安装指定工具"""
        if tool_name not in self.SUPPORTED_TOOLS:
            logger.error(f"不支持的工具: {tool_name}")
            return False

        # 检查依赖
        if not self.check_dependencies(tool_name):
            return False

        # 执行安装命令
        return self._install_single_tool(tool_name)

    def _install_single_tool(self, tool_name):
        """安装单个工具（内部使用）"""
        tool_info = self.SUPPORTED_TOOLS[tool_name]
        logger.info(f"开始安装 {tool_name}...")
        
        with console.status(f"[bold green]安装 {tool_name} 中..."):
            result, success = run_command(tool_info["install_command"])
            
            if success:
                logger.info(f"{tool_name} 安装成功!")
            else:
                logger.error(f"{tool_name} 安装失败: {result.stderr}")
        
        return success

    def choose_and_install(self):
        """选择并安装一个或多个工具"""
        logger.info("可用工具:")
        tool_list = list(self.SUPPORTED_TOOLS.items())
        for i, (name, info) in enumerate(tool_list, 1):
            logger.info(f"{i}. {name}: {info['description']}")

        choices = [str(i) for i in range(1, len(tool_list) + 1)]
        choice = Prompt.ask(
            "请选择要安装的工具（可输入多个编号，用逗号分隔，如: 1,2）",
            default="1"
        )
        
        # 解析用户输入的多个选择
        selected_indices = []
        for c in choice.split(','):
            c = c.strip()
            if c in choices:
                selected_indices.append(int(c) - 1)
            else:
                logger.warning(f"无效的选择: {c}，将被忽略")
        
        if not selected_indices:
            logger.error("没有有效的选择，退出安装")
            return False
        
        # 收集所有需要安装的工具和依赖
        selected_tools = [tool_list[i][0] for i in selected_indices]
        all_dependencies = set()
        for tool_name in selected_tools:
            all_dependencies.update(self.SUPPORTED_TOOLS[tool_name]["dependencies"])
        
        # 检查并安装所有依赖
        logger.info(f"需要安装的工具: {', '.join(selected_tools)}")
        logger.info(f"检测到所有需要的依赖: {', '.join(all_dependencies)}")
        
        missing_deps = [dep for dep in all_dependencies if not check_command_exists(dep)]
        
        if missing_deps:
            logger.warning(f"检测到缺失依赖: {', '.join(missing_deps)}")
            install = Prompt.ask(f"是否要安装这些依赖?", choices=["y", "n"], default="y")
            if install.lower() == "y":
                if not self.install_dependencies(missing_deps):
                    logger.error("依赖安装失败，无法继续")
                    return False
            else:
                logger.error("依赖缺失，无法继续安装工具")
                return False
        
        # 安装所有选择的工具
        all_success = True
        with Progress() as progress:
            task = progress.add_task("[green]安装工具...", total=len(selected_tools))
            
            for tool_name in selected_tools:
                progress.update(task, description=f"[green]安装 {tool_name}...")
                success = self._install_single_tool(tool_name)
                if not success:
                    all_success = False
                progress.update(task, advance=1)
        
        if all_success:
            logger.info("所有选择的工具都已成功安装!")
        else:
            logger.warning("部分工具安装失败，请查看日志了解详情")
        
        return all_success