# AI Coding Kit

一个跨平台的AI工具集成项目，帮助开发者轻松安装和管理各类AI开发工具。

## 支持的工具

- **openspec**: Fission AI 的开放规范工具
- **spec-kit**: GitHub 的规范工具包

## 特点

- 跨平台支持 (Linux, macOS, Windows)
- 支持同时安装多个工具
- 自动检测和安装依赖
- 使用 `uv` 进行快速安装
- 美观的富文本日志输出

## wechat group
- add v: youandme10086 , to join wechat group for ai 微信群.

|wechat|wechat-group|
|------|----------|
|![wechat](https://gitee.com/zengfr/n8n-workflow-all-templates/raw/main/img/1wechat.jpg)|![wechat-group](https://gitee.com/zengfr/n8n-workflow-all-templates/raw/main/img/2wechat-group.jpg)|

## 安装

首先，确保您的系统已安装 Python 3.12 或更高版本。

使用 `uv` 安装（推荐）：

```bash
uv tool install ai-coding-kit --from git+https://github.com/zengfr/ai-coding-kit.git
# 或者如果您在项目目录中
uv install
```

使用 pip 安装：

```bash
pip install .
```

## 使用方法

1. 安装完成后，在命令行中运行：

```bash
ai-coding-kit
```

2. 程序会显示支持的工具列表，输入要安装的工具编号（可输入多个，用逗号分隔）并按回车：

```
1. openspec: Open specification tool from Fission AI
2. spec-kit: Specification kit from GitHub
请选择要安装的工具（可输入多个编号，用逗号分隔，如: 1,2） [1]: 1,2
```

3. 程序会自动检测并统一安装所有所需的依赖（如 npm, uv, git 等）

4. 之后会依次安装您选择的所有工具

5. 安装完成后，会显示总体安装结果

## 依赖说明

不同工具需要不同的依赖，程序会自动检测并提示安装：

- **openspec** 需要: npm (Node.js 包管理器)
- **spec-kit** 需要: uv (Python 包管理器) 和 git (版本控制系统)

## 平台特定说明

### Windows

- 部分工具可能需要管理员权限进行安装
- 建议使用 PowerShell 而非 cmd 以获得最佳体验

### macOS

- 如果没有安装 Homebrew，可能需要手动安装部分依赖
- 对于系统完整性保护 (SIP) 限制的目录，可能需要使用 sudo

### Linux

- 程序会自动检测并使用 apt 或 yum 包管理器
- 可能需要输入 sudo 密码以安装系统依赖

## 问题解决

如果安装过程中遇到问题，请检查：

1. 您是否有足够的权限进行安装（必要时使用 sudo 或管理员权限）
2. 您的网络连接是否正常
3. 您的操作系统是否满足最低要求

如需进一步帮助，请提交 issue 到项目仓库。
```

## 功能亮点

1. **多工具同时安装** - 支持通过逗号分隔的编号选择多个工具同时安装
2. **智能依赖管理** - 自动检测并统一安装所有选中工具的依赖，避免重复安装
3. **跨平台支持** - 针对Linux、macOS和Windows分别优化安装流程
4. **直观的进度展示** - 使用rich库提供美观的进度条和日志输出
5. **灵活的安装选项** - 支持uv快速安装，也兼容传统的pip安装方式

这个项目满足了所有需求，提供了简洁易用的界面，让用户能够轻松安装所需的AI开发工具。