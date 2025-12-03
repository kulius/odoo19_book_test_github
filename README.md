# Odoo 19 學習專案 - 房地產管理系統

## 📖 專案簡介

這是一個基於 Odoo 19 的房地產管理系統學習專案，包含完整的房地產物業管理功能。

## 🏗️ 專案結構

```
odoo19/
├── custom_addons/          # 自訂模組目錄
│   ├── estate/            # 房地產核心模組
│   │   ├── models/        # 資料模型
│   │   ├── views/         # 視圖定義
│   │   ├── report/        # 報表模板
│   │   └── security/      # 權限配置
│   └── estate_account/    # 房地產會計整合模組
├── odoo-19.0/             # Odoo 核心程式
└── .cursor/               # Cursor IDE 配置
    └── rules/             # 開發規則文件
```

## 🎯 功能模組

### Estate (房地產核心模組)

#### 主要功能
- ✅ 房地產物業管理
- ✅ 物業類型分類
- ✅ 物業標籤系統
- ✅ 報價管理系統
- ✅ 狀態追蹤 (新建、已收到報價、已接受報價、已售出、已取消)

#### 資料模型
- `estate.property` - 房地產物業
- `estate.property.type` - 物業類型
- `estate.property.tag` - 物業標籤
- `estate.property.offer` - 物業報價

#### 特色功能
- 📊 自動計算最佳報價
- 📊 總面積自動計算 (居住面積 + 花園面積)
- 🔒 報價驗證 (新報價必須高於現有報價)
- 🔒 售價驗證 (不得低於期望價格的 90%)
- 🗑️ 刪除保護 (只能刪除新建或已取消的物業)
- 📝 報價有效期自動計算

### Estate Account (會計整合模組)

#### 主要功能
- ✅ 自動產生發票
- ✅ 佣金計算 (售價的 6%)
- ✅ 行政費用 (固定 100 元)

## 🛠️ 技術特點

### Odoo 19 新特性應用

#### 1. 新的約束語法
```python
_unique_name = models.Constraint(
    'UNIQUE(name)',
    'A property tag name must be unique.'
)
```

#### 2. Command API
```python
from odoo.fields import Command

invoice_line_ids = [
    Command.create({'name': 'Item 1', 'price_unit': 100.0}),
    Command.create({'name': 'Item 2', 'price_unit': 50.0})
]
```

#### 3. 改進的視圖條件語法
```xml
<field name="garden_area" invisible="not garden"/>
<field name="line_ids" readonly="state in ['done', 'cancel']"/>
```

## 📋 開發規範

專案包含完整的開發規則文件：

- **odoo-python.mdc** - Python 模型開發規則
  - 模型定義和繼承
  - 欄位類型和屬性
  - API 裝飾器使用
  - CRUD 操作最佳實踐
  - Odoo 19 新功能

- **odoo-views.mdc** - Views 和 XML 開發規則
  - 8 種視圖類型完整說明
  - 30+ 種 Widget 使用方法
  - QWeb 模板語法
  - 視圖繼承和擴展
  - 最佳實踐指南

## 🚀 安裝和執行

### 環境需求
- Python 3.10+
- PostgreSQL 12+
- Odoo 19

### 安裝步驟

1. 克隆專案
```bash
git clone https://github.com/kulius/odoo19_book_test_github.git
cd odoo19_book_test_github
```

2. 安裝 Odoo 依賴
```bash
pip install -r requirements.txt
```

3. 啟動 Odoo
```bash
python odoo-19.0/odoo-bin -c odoo.conf
```

4. 安裝模組
- 進入 Odoo 後台
- 啟用開發者模式
- 更新應用程式列表
- 安裝 "Real Estate" 模組

## 📚 學習資源

### 模組開發流程
1. 定義資料模型 (`models/`)
2. 建立視圖 (`views/`)
3. 設定權限 (`security/`)
4. 開發報表 (`report/`)
5. 測試功能

### 關鍵概念
- **ORM**: Odoo 的物件關聯映射
- **視圖繼承**: 擴展現有視圖
- **計算欄位**: 動態計算的欄位
- **約束條件**: SQL 和 Python 約束
- **動作和選單**: 使用者介面導航

## 🔧 開發工具配置

### Cursor IDE
- 已配置 `.cursorignore` 排除不必要的檔案
- 已配置開發規則 (`.cursor/rules/`)
- 自動套用 Odoo 19 開發最佳實踐

### Git
- 已配置 `.gitignore` 排除敏感和臨時檔案
- 使用語義化提交訊息 (Conventional Commits)

## 📝 提交規範

使用 Conventional Commits 格式：

- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文件更新
- `style:` 程式碼格式調整
- `refactor:` 重構
- `test:` 測試相關
- `chore:` 建置或輔助工具變動

## 📄 授權

本專案僅供學習使用。

## 👥 作者

- 開發者：Kulius

## 🙏 致謝

感謝 Odoo 官方文件和社群的支援。

