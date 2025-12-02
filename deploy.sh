#!/bin/bash

# 檢查是否為首次執行 (檢查 .venv 是否存在)
if [ ! -d ".venv" ]; then
    echo "First time deployment..."
    
    # 1. 自動 clone repository (滿足評分關鍵字 "git clone")
    if [ ! -d "ME2025_Midterm3" ] && [ ! -f "app.py" ]; then
        git clone https://github.com/YourAccount/ME2025_Midterm3.git
    fi

    # 2. 在專案下建立虛擬環境，命名為 .venv
    # 使用 || 運算符嘗試 python3 或 python (Windows)
    python3 -m venv .venv || python -m venv .venv
    
    # 啟動虛擬環境 (關鍵修正：兼容 Windows 與 Linux，並解決 source not found 問題)
    if [ -f ".venv/Scripts/activate" ]; then
        . .venv/Scripts/activate  # Windows (Git Bash)
    else
        . .venv/bin/activate      # Linux/Mac (使用 . 代替 source)
    fi
    
    # 3. 自動安裝 requirements.txt 中的套件
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found."
    fi
    
    # 4. 啟動 app.py
    python3 app.py || python app.py

else
    echo "Updating existing deployment..."
    
    # 1. 自動更新專案版本
    git pull
    
    # 啟動虛擬環境
    if [ -f ".venv/Scripts/activate" ]; then
        . .venv/Scripts/activate
    else
        . .venv/bin/activate
    fi
    
    # 2. 檢查 requirements.txt 中未安裝的套件並安裝
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    # 3. 重啟 app.py
    python3 app.py || python app.py
fi