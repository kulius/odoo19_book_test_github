# Project Context

## Purpose
Odoo 19 企業資源規劃 (ERP) 系統開發專案，專注於建立高品質、可維護的自訂模組，遵循 Odoo 官方最佳實踐。

## Tech Stack
- **Framework**: Odoo 19.0 (Python 3.10+)
- **Backend**: Python 3.10+ with Odoo ORM
- **Frontend**: Odoo Web Framework (JavaScript/Owl Components)
- **Database**: PostgreSQL
- **Views**: XML (QWeb Templates)
- **Version Control**: Git with GitHub integration

## Project Conventions

### Code Style
- **Python**: 嚴格遵守 [Odoo Python 編碼指南](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html)
  - 使用 4 空格縮排
  - 遵循 PEP 8 命名規範
  - 使用 `api.depends`, `api.constrains`, `api.onchange` 等裝飾器
  - 優先使用 `@api.model_create_multi` 而非 `@api.model` 的 create
  
- **XML**: 遵循 Odoo 視圖結構規範
  - 使用 2 空格縮排
  - 遵循命名慣例：`model_name_view_type` (例如：`estate_property_view_form`)
  - 視圖 ID 格式：`module.model_name_view_type`

- **命名規範**:
  - 模型名稱：`module.model` (例如：`estate.property`)
  - 欄位名稱：snake_case (例如：`date_availability`)
  - 類別名稱：PascalCase (例如：`EstateProperty`)
  - 方法名稱：snake_case (例如：`action_confirm`)

### Architecture Patterns

#### 模組結構 (強制)
```
module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── model_name.py
├── views/
│   ├── model_name_views.xml
│   └── model_name_menus.xml
├── security/
│   └── ir.model.access.csv
├── data/           # 可選
├── report/         # 可選
└── static/         # 可選
```

#### ORM 模式
- 使用 `self.env['model.name']` 存取其他模型
- 使用 `fields.Command` API 操作 One2many/Many2many 關係
- 計算欄位使用 `@api.depends` 並設定 `store=True` (當需要時)
- 使用 `models.Constraint` (Odoo 19 新語法) 定義 SQL 約束

#### 視圖繼承原則 (不容協商)
1. **必須讀取原始碼**: 繼承視圖前，必須讀取 `C:\odoo19\odoo-19.0\addons` 中的原始視圖
2. **精確 XPath**: 生成最小化、精確的 XPath 表達式，只選取單一元素
3. **參考標準模組**: 優先參考 `sale`、`account` 模組的視圖結構
4. **避免脆弱程式碼**: 不使用過於寬泛或依賴結構假設的 XPath

### Testing Strategy
- 使用 Odoo 內建測試框架 (`odoo.tests`)
- 測試檔案放置於 `tests/` 目錄
- 測試類別繼承 `odoo.tests.TransactionCase` 或 `odoo.tests.HttpCase`
- 命名規範：`test_*.py`

### Git Workflow
- **分支策略**: Feature Branch Workflow
  - `main`: 穩定生產版本
  - `develop`: 開發整合分支
  - `feature/*`: 功能開發分支
  
- **Commit 規範**:
  - 格式：`[MODULE] type: description`
  - 類型：`feat`, `fix`, `refactor`, `docs`, `style`, `test`
  - 範例：`[estate] feat: add property offer management`

- **Pull Request**: 
  - 歸檔變更時 (`openspec archive`) 自動建立 PR
  - PR 標題格式：`[OpenSpec] Archive: change-id`
  - 包含完整的變更說明和測試結果

## Domain Context

### Odoo 核心概念
- **Models**: 資料模型，繼承 `models.Model`, `models.TransientModel`, 或 `models.AbstractModel`
- **Fields**: 欄位類型包括 Char, Text, Integer, Float, Boolean, Date, Datetime, Selection, Many2one, One2many, Many2many 等
- **Views**: 視圖類型包括 form, list (tree), kanban, calendar, graph, pivot, search, activity
- **Actions**: ir.actions.act_window, ir.actions.server, ir.actions.report
- **Security**: 存取權限 (ir.model.access) 和記錄規則 (ir.rule)

### 參考路徑
- **Odoo 原始碼**: `C:\odoo19\odoo-19.0\addons`
- **標準參考模組**: 
  - `sale`: 銷售管理 (視圖、工作流程參考)
  - `account`: 會計管理 (複雜表單、計算欄位參考)
- **自訂模組**: `C:\odoo19\custom_addons`
- **學習範例**: `C:\odoo19\book_addons` (包含 estate 模組的演進版本)

## Important Constraints

### 治理層 (Governance Layer) - 不容協商的開發原則

#### 1. ORM 規範 (強制)
- **必須**嚴格遵守 [Odoo Python 編碼指南](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html)
- **必須**使用正確的 API 裝飾器 (`@api.depends`, `@api.constrains`, `@api.onchange`)
- **必須**使用 `fields.Command` API 操作關聯欄位 (不使用舊的 tuple 語法)
- **必須**在 `create` 方法中使用 `@api.model_create_multi` (Odoo 19 推薦)
- **必須**使用 `models.Constraint` 定義 SQL 約束 (Odoo 19 新語法)
- **禁止**在迴圈中執行 ORM 查詢 (使用 `mapped()`, `filtered()` 等批量操作)

#### 2. 建立 XML 視圖前的強制檢查
- **必須**先讀取 `C:\odoo19\odoo-19.0\addons` 中的相關原始碼
- **必須**優先參考 `sale` 和 `account` 模組的視圖結構
- **必須**遵循視圖類型的標準結構：
  - `<form>`: header → sheet → (button_box → title → group → notebook) → chatter
  - `<list>`: header (可選) → field 列表
  - `<kanban>`: progressbar → templates → card
  - `<search>`: field → separator → filter → group
- **必須**使用正確的 widget 和屬性
- **禁止**自行猜測或假設視圖結構

#### 3. 繼承 XML 視圖的強制規則
- **必須**在繼承前讀取 `C:\odoo19\odoo-19.0\addons` 中要繼承的原始視圖
- **必須**生成精確且最小化的 XPath 表達式
- **必須**XPath 只選取單一元素 (避免選取多個元素導致不可預測行為)
- **必須**驗證 XPath 的唯一性和穩定性
- **禁止**使用過於寬泛的 XPath (例如：`//field` 而不指定屬性)
- **禁止**依賴視圖內部結構的假設 (例如：假設某欄位一定在某 group 內)
- **推薦**使用 `position="attributes"` 修改屬性，而非 `replace` 整個元素

#### 4. 命名與結構規範 (強制)
- **必須**遵守 Odoo 19 模組目錄結構
- **必須**使用標準命名慣例：
  - 視圖 ID: `model_name_view_type` (例如：`estate_property_view_form`)
  - 動作 ID: `action_model_name` (例如：`action_estate_property`)
  - 選單 ID: `menu_model_name` (例如：`menu_estate_property`)
  - 模型檔案: `model_name.py` (例如：`estate_property.py`)
  - 視圖檔案: `model_name_views.xml` (例如：`estate_property_views.xml`)
- **必須**在 `__manifest__.py` 中正確聲明依賴和資料檔案
- **必須**在 `__init__.py` 中正確導入模組

#### 5. 歸檔與版本控制 (強制)
- **必須**在執行 `openspec archive <change-id>` 時自動將程式碼推送至 GitHub
- **必須**依據 OpenSpec 規格內容自動建立 Pull Request
- **必須**在 PR 中包含：
  - 變更摘要 (從 `proposal.md` 提取)
  - 完成的任務清單 (從 `tasks.md` 提取)
  - 相關的規格變更 (從 delta specs 提取)
  - 測試結果和截圖 (如適用)
- **必須**使用分支命名：`openspec/<change-id>`
- **必須**PR 標題格式：`[OpenSpec] <change-id>: <brief description>`

#### 6. 程式碼品質檢查 (強制)
- **必須**在提交前執行 `openspec validate --strict`
- **必須**確保沒有 Python 語法錯誤
- **必須**確保 XML 格式正確且可解析
- **必須**確保所有必要的安全規則已定義
- **推薦**使用 `ruff` 或 `pylint` 進行 Python 程式碼檢查

### 違規處理
- 任何違反上述治理層原則的程式碼**必須**被拒絕
- AI 助手**必須**在實作前確認已遵守所有強制規則
- 如有疑問，**必須**先詢問並確認，而非假設或猜測

## External Dependencies

### Odoo 原始碼參考
- **路徑**: `C:\odoo19\odoo-19.0\addons`
- **用途**: 視圖結構參考、繼承目標、最佳實踐範例
- **關鍵模組**:
  - `base`: 核心功能、基礎模型
  - `web`: Web 框架、UI 元件
  - `sale`: 銷售管理、工作流程範例
  - `account`: 會計管理、複雜表單範例
  - `stock`: 庫存管理、進階 ORM 使用
  - `project`: 專案管理、看板視圖範例

### 開發工具
- **Odoo CLI**: `odoo-bin` (位於 `C:\odoo19\odoo-19.0\odoo-bin`)
- **OpenSpec CLI**: `openspec` (用於規格管理和變更追蹤)
- **資料庫**: PostgreSQL (本地開發環境)

### 文件資源
- [Odoo 19 官方文件](https://www.odoo.com/documentation/19.0/)
- [Odoo 開發者指南](https://www.odoo.com/documentation/19.0/developer.html)
- [Odoo Python 編碼指南](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html)

## AI 助手特別注意事項

### 實作前檢查清單
- [ ] 已讀取 `openspec/project.md` (本文件)
- [ ] 已讀取相關的 OpenSpec 規格 (`openspec/specs/`)
- [ ] 已檢查是否有衝突的進行中變更 (`openspec list`)
- [ ] 如需繼承視圖，已讀取原始視圖檔案
- [ ] 如需建立新視圖，已參考 `sale` 或 `account` 模組
- [ ] 已確認遵守所有治理層的強制規則

### 常見錯誤與避免方法
1. **錯誤**: 在繼承視圖時未讀取原始視圖，導致 XPath 錯誤
   - **避免**: 必須先使用 `read_file` 讀取原始視圖

2. **錯誤**: 使用過於寬泛的 XPath，選取了多個元素
   - **避免**: 使用具體的屬性選擇器，確保只選取一個元素

3. **錯誤**: 在迴圈中執行 ORM 查詢，導致效能問題
   - **避免**: 使用 `mapped()`, `filtered()`, `browse()` 等批量操作

4. **錯誤**: 使用舊的 tuple 語法操作關聯欄位
   - **避免**: 使用 `fields.Command` API (Odoo 19 推薦)

5. **錯誤**: 未在 `__manifest__.py` 中聲明依賴
   - **避免**: 確保所有依賴模組都在 `depends` 列表中

### 工作流程
1. **規劃階段**: 建立 OpenSpec 變更提案
2. **實作階段**: 遵循 `tasks.md` 逐步實作
3. **驗證階段**: 執行 `openspec validate --strict`
4. **測試階段**: 在 Odoo 中測試功能
5. **歸檔階段**: 執行 `openspec archive <change-id>` 並自動建立 PR
