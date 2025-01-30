Write-Host "Starting package process..." -ForegroundColor Green

# 清理之前的构建文件
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
Get-ChildItem "*.spec" | Remove-Item

# 设置环境变量
$env:PYTHONIOENCODING = "utf-8"

# 执行打包命令（使用英文名称）
$command = @"
pyinstaller --onefile --windowed --icon="logo(1).png" --add-data="logo.png;." --add-data="config.py;." --add-data="qr_generator.py;." --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=PyQt6 --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets --collect-all=qrcode --name="QRPaperGenerator" main.py
"@

Write-Host "Executing package command..." -ForegroundColor Yellow
Invoke-Expression $command

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nPackage completed!" -ForegroundColor Green
    
    # 重命名为中文名称
    $englishName = "dist\QRPaperGenerator.exe"
    $chineseName = "dist\贝朵亚画纸生成系统.exe"
    
    if (Test-Path $englishName) {
        Write-Host "Renaming executable file..." -ForegroundColor Yellow
        Rename-Item -Path $englishName -NewName $chineseName -Force
        Write-Host "Executable file location: $chineseName" -ForegroundColor Cyan
    } else {
        Write-Host "Error: Cannot find the generated executable file!" -ForegroundColor Red
    }
} else {
    Write-Host "`nPackage failed!" -ForegroundColor Red
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 
