# PyInstaller 打包指南

## GitHub Actions 自动化构建 Windows EXE

### 准备工作
1. 创建 GitHub 仓库并推送代码
2. 准备 256x256 像素的 Windows 图标文件 `app.ico`

### 配置构建流程
1. 创建 `.github/workflows/build.yml` 文件
2. 配置文件内容：
```yaml
name: Build Windows EXE

on:
  push:
    tags:
      - 'v*'  # 仅标签推送触发构建

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python 3.8
      uses: actions/setup-python@v4
      with:
        python-version: "3.8"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Build EXE
      run: |
        pyinstaller --windowed --onefile \
          --name WDFConverter \
          --icon=app.ico \
          main.py

    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ReleasePackage
        path: |
          dist/WDFConverter.exe
          README.md
```

### 使用流程
1. 创建版本标签并推送
```bash
git tag v1.0.0
git push origin --tags
```
2. 在 GitHub 仓库的 Actions 标签页查看构建进度
3. 构建完成后在 Artifacts 下载 EXE 文件

### 高级配置（可选）
```yaml
# 自动创建 GitHub Release
- name: Create Release
  uses: softprops/action-gh-release@v1
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: |
      dist/WDFConverter.exe
      README.md
```

## 本地打包命令（Windows环境）
```bash
pyinstaller --windowed --onefile \
  --name WDFConverter \
  --icon=app.ico \
  --add-data "app.ico;." \
  main.py
```

## 打包原理说明
1. 文件包含内容：
   - 嵌入式 Python 解释器
   - 压缩的依赖库（PyQt6、renishawWiRE）
   - 编译后的字节码
   - 资源文件（图标等）

2. 反编译防护建议：
   - 使用 pyarmor 混淆代码
   - 添加代码签名证书

## 验证打包结果
1. 在无 Python 环境的 Windows 系统运行
2. 使用 Dependency Walker 检查依赖
3. 使用 PE 文件分析工具查看结构

## 常见问题排查
```markdown
1. 报错 "Failed to execute script"
   - 检查控制台输出：在cmd中运行 `WDFConverter.exe`
   
2. 缺少图标文件
   - 确认 app.ico 存在且为有效ICO格式
   - 使用在线转换工具生成标准ICO文件

3. 防病毒软件误报
   - 提交到 VirusTotal 添加白名单
   - 使用代码签名证书
```
