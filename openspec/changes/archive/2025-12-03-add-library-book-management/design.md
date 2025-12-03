# Design: 圖書館管理系統 - 圖書資訊管理

## Context
這是一個全新的 Odoo 模組，為學校圖書館提供數位化的圖書管理解決方案。本設計文件專注於系統的第一個核心功能：**圖書資訊管理**。

### 背景
- 目標使用者：學校圖書館管理員和讀者
- 現有系統：無（全新開發）
- 技術環境：Odoo 19, PostgreSQL
- 部署位置：`custom_addons/library_management/`

### 約束條件
- 必須遵守 Odoo 19 開發規範和專案治理層原則
- 必須參考 Odoo 原始碼（特別是 `sale` 和 `account` 模組）設計視圖
- 必須使用 Odoo 19 新語法（如 `models.Constraint`, `fields.Command`）
- 必須支援多使用者和權限控制

## Goals / Non-Goals

### Goals
- ✅ 提供完整的圖書 CRUD 功能
- ✅ 實作圖書分類系統，便於管理和查詢
- ✅ 提供直觀的使用者介面（列表、表單、看板、搜尋）
- ✅ 實作庫存追蹤功能
- ✅ 支援圖片上傳（書籍封面）
- ✅ 整合 Odoo 訊息追蹤功能（mail.thread）
- ✅ 實作適當的資料驗證和約束
- ✅ 設定權限控制（管理員 vs 一般使用者）

### Non-Goals
- ❌ 借閱管理功能（將在後續變更中實作）
- ❌ 讀者管理功能（將在後續變更中實作）
- ❌ 報表功能（將在後續變更中實作）
- ❌ 與外部圖書資料庫 API 整合（未來可考慮）
- ❌ 條碼掃描功能（未來可考慮）

## Decisions

### 1. 資料模型設計

#### 決策：使用兩個主要模型
- **`library.book.category`**: 圖書分類
- **`library.book`**: 圖書資訊

**理由**：
- 分離關注點，便於維護和擴展
- 分類可重複使用，避免資料冗餘
- 符合 Odoo 最佳實踐（如 `product.category` 的設計）

#### 替代方案考慮：
- **方案 A**: 使用 Selection 欄位儲存分類
  - ❌ 缺乏彈性，新增分類需要修改程式碼
  - ❌ 無法儲存分類的額外資訊（如描述）
- **方案 B**: 使用 Many2many 關係支援多分類
  - ⚠️ 增加複雜度，目前需求不需要
  - 💡 未來可考慮升級為 Many2many

### 2. 庫存管理策略

#### 決策：使用兩個欄位追蹤庫存
- `quantity`: 總庫存數量（Integer）
- `available_quantity`: 可借閱數量（Integer）

**理由**：
- 簡單直觀，易於理解和維護
- 為未來的借閱管理預留介面
- 可透過計算欄位 `is_available` 快速判斷可借閱狀態

#### 替代方案考慮：
- **方案 A**: 只使用 `quantity`，借閱時扣除
  - ❌ 無法追蹤總館藏數量
  - ❌ 歸還時難以驗證數量正確性
- **方案 B**: 整合 Odoo 的 `stock` 模組
  - ❌ 過度複雜，圖書館不需要完整的庫存管理功能
  - ❌ 增加不必要的依賴

### 3. ISBN 處理

#### 決策：使用 Char 欄位儲存 ISBN，並實作格式驗證
- 欄位類型：`fields.Char(size=13)`
- 驗證：Python 約束檢查 ISBN-10 或 ISBN-13 格式
- 唯一性：SQL 約束確保 ISBN 唯一

**理由**：
- ISBN 可能包含連字號，使用字串更合適
- 支援 ISBN-10 和 ISBN-13 兩種格式
- 唯一性約束防止重複錄入

#### 替代方案考慮：
- **方案 A**: 使用 Integer 儲存
  - ❌ 無法處理連字號
  - ❌ ISBN-13 可能超出整數範圍
- **方案 B**: 不驗證格式
  - ❌ 可能導致資料品質問題

### 4. 視圖設計策略

#### 決策：參考 Odoo `sale` 模組的視圖結構
- 表單視圖：使用 header + sheet + chatter 結構
- 列表視圖：使用 decoration 標示庫存狀態
- 看板視圖：卡片式佈局，顯示封面圖片
- 搜尋視圖：提供多維度過濾和分組

**理由**：
- 符合 Odoo 標準 UX 模式，使用者熟悉
- 遵守專案治理層要求（參考標準模組）
- 提供一致的使用者體驗

#### 關鍵視圖元素：
1. **表單視圖**：
   - Button box：顯示統計資訊（未來可擴展）
   - Title：書名（大標題）
   - Group：基本資訊（ISBN、作者、出版社等）
   - Notebook：分頁顯示詳細資訊和描述
   - Chatter：訊息追蹤和活動

2. **列表視圖**：
   - Decoration：`decoration-danger="available_quantity == 0"` 標示無庫存
   - Decoration：`decoration-success="available_quantity > 0"` 標示有庫存
   - Optional fields：允許使用者自訂顯示欄位

3. **看板視圖**：
   - 顯示書籍封面圖片
   - 預設依分類分組
   - 快速查看庫存狀態

### 5. 權限設計

#### 決策：兩層權限結構
- **Library User** (group_library_user): 一般使用者
  - 可讀取所有書籍資訊
  - 可查詢和瀏覽
- **Library Manager** (group_library_manager): 圖書管理員
  - 繼承 Library User 的所有權限
  - 可新增、編輯、刪除書籍
  - 可管理分類

**理由**：
- 符合圖書館實際使用情境
- 保護資料不被誤操作
- 為未來的借閱管理預留權限擴展空間

#### 替代方案考慮：
- **方案 A**: 所有人都可編輯
  - ❌ 缺乏資料保護
  - ❌ 容易造成資料混亂
- **方案 B**: 更細緻的權限（如分離新增/編輯/刪除）
  - ⚠️ 過度複雜，目前需求不需要

### 6. 資料驗證策略

#### 決策：多層驗證機制
1. **SQL 約束**（資料庫層）：
   - ISBN 唯一性
   - 數量非負（quantity >= 0, available_quantity >= 0）
   - 分類代碼唯一性

2. **Python 約束**（應用層）：
   - ISBN 格式驗證（10 或 13 位數字）
   - 可借閱數量不超過總數量（available_quantity <= quantity）

3. **欄位屬性**（UI 層）：
   - Required 欄位：name, isbn, category_id, quantity
   - Domain 限制：category_id 只顯示 active 的分類

**理由**：
- 多層防護確保資料完整性
- SQL 約束提供最強保證
- Python 約束提供更複雜的業務邏輯驗證
- UI 限制提供即時反饋

## Architecture

### 模組結構
```
library_management/
├── __init__.py                          # 模組初始化
├── __manifest__.py                      # 模組清單
├── models/
│   ├── __init__.py                      # 模型初始化
│   ├── library_book.py                  # 圖書模型
│   └── library_book_category.py         # 分類模型
├── views/
│   ├── library_book_views.xml           # 圖書視圖
│   ├── library_book_category_views.xml  # 分類視圖
│   └── library_menus.xml                # 選單和動作
├── security/
│   ├── library_security.xml             # 使用者群組
│   └── ir.model.access.csv              # 存取權限
├── data/
│   └── library_book_category_data.xml   # 預設分類資料
└── static/
    └── description/
        └── icon.png                     # 模組圖示
```

### 資料模型關係
```
library.book.category (1) ----< (N) library.book
    - id
    - name                              - id
    - code                              - name
    - description                       - isbn
    - active                            - author
                                        - publisher
                                        - publish_date
                                        - category_id (Many2one)
                                        - quantity
                                        - available_quantity
                                        - description
                                        - cover_image
                                        - pages
                                        - language
                                        - is_available (computed)
```

### 關鍵欄位定義

#### library.book
```python
# 基本資訊
name = fields.Char(string="書名", required=True, index=True, tracking=True)
isbn = fields.Char(string="ISBN", size=13, required=True, index=True, copy=False)
author = fields.Char(string="作者", required=True, index=True)
publisher = fields.Char(string="出版社")
publish_date = fields.Date(string="出版日期")

# 分類和庫存
category_id = fields.Many2one('library.book.category', string="分類", required=True, 
                              ondelete='restrict', index=True)
quantity = fields.Integer(string="總數量", required=True, default=1)
available_quantity = fields.Integer(string="可借閱數量", required=True, default=1)

# 額外資訊
description = fields.Text(string="簡介")
cover_image = fields.Image(string="封面圖片", max_width=1024, max_height=1024)
pages = fields.Integer(string="頁數")
language = fields.Selection([
    ('zh_TW', '繁體中文'),
    ('zh_CN', '簡體中文'),
    ('en', 'English'),
    ('ja', '日本語'),
], string="語言", default='zh_TW')

# 計算欄位
is_available = fields.Boolean(string="可借閱", compute='_compute_is_available', 
                               store=True)
```

#### library.book.category
```python
name = fields.Char(string="分類名稱", required=True, translate=True)
code = fields.Char(string="分類代碼", required=True, size=10)
description = fields.Text(string="描述")
active = fields.Boolean(string="啟用", default=True)
book_count = fields.Integer(string="書籍數量", compute='_compute_book_count')
```

## Risks / Trade-offs

### 風險 1: ISBN 資料品質
- **風險**: 使用者可能輸入錯誤的 ISBN 或重複的 ISBN
- **緩解**: 
  - 實作 ISBN 格式驗證
  - SQL 唯一性約束防止重複
  - UI 提示正確的 ISBN 格式

### 風險 2: 庫存數量不一致
- **風險**: `available_quantity` 可能與實際可借閱數量不符
- **緩解**:
  - Python 約束確保 `available_quantity <= quantity`
  - 未來實作借閱管理時，自動更新 `available_quantity`
  - 提供庫存校正功能（未來）

### 風險 3: 效能問題（大量書籍）
- **風險**: 當書籍數量超過 10,000 筆時，列表視圖可能變慢
- **緩解**:
  - 在關鍵欄位（name, isbn, author, category_id）建立索引
  - 使用分頁和限制（Odoo 預設）
  - 提供高效的搜尋和過濾功能
  - 未來可考慮加入快取機制

### 權衡 1: 簡單 vs 完整
- **選擇**: 簡單的庫存管理（兩個整數欄位）
- **權衡**: 犧牲了複雜的庫存追蹤功能（如歷史記錄、多地點庫存）
- **理由**: 符合圖書館的實際需求，避免過度設計

### 權衡 2: 單一分類 vs 多分類
- **選擇**: 每本書只能屬於一個分類（Many2one）
- **權衡**: 無法為書籍設定多個分類標籤
- **理由**: 簡化管理，符合大多數圖書館的分類方式
- **未來**: 可升級為 Many2many 支援多分類

## Migration Plan

### 初始部署
1. 在 Odoo 中安裝模組
2. 匯入預設分類資料
3. 訓練圖書管理員使用系統
4. 逐步匯入現有書籍資料

### 資料匯入策略
- 提供 CSV 匯入範本
- 使用 Odoo 內建的匯入功能
- 驗證匯入資料的完整性

### 回滾計畫
- 解除安裝模組會保留資料（Odoo 預設行為）
- 如需完全移除，需手動刪除資料表
- 建議在測試環境先驗證

## Open Questions

### 已解決的問題
- ✅ **Q**: 是否需要支援電子書？
  - **A**: 第一版不支援，未來可透過新增 `book_type` 欄位擴展

- ✅ **Q**: 是否需要支援多語言？
  - **A**: 分類名稱支援翻譯（translate=True），書籍資訊不翻譯

### 待確認的問題
- ⏳ **Q**: 是否需要支援書籍的多個版本（如第一版、第二版）？
  - **建議**: 第一版將不同版本視為不同書籍，未來可考慮加入版本管理

- ⏳ **Q**: 是否需要支援書籍的條碼掃描？
  - **建議**: 第一版不支援，未來可透過整合條碼掃描 API 實作

- ⏳ **Q**: 圖書分類是否需要支援階層結構（如主分類 > 子分類）？
  - **建議**: 第一版使用扁平結構，如需要可在未來版本加入 `parent_id` 欄位

## Implementation Notes

### 必須遵守的規範
1. **讀取原始碼**: 實作視圖前，必須讀取 `C:\odoo19\odoo-19.0\addons\sale` 和 `account` 模組的視圖
2. **使用新語法**: 使用 `models.Constraint` 而非舊的 `_sql_constraints`
3. **命名規範**: 嚴格遵守 `model_name_view_type` 格式
4. **程式碼品質**: 執行 `openspec validate --strict` 確保無錯誤

### 參考檔案
- 表單視圖參考: `C:\odoo19\odoo-19.0\addons\sale\views\sale_order_views.xml`
- 列表視圖參考: `C:\odoo19\odoo-19.0\addons\account\views\account_move_views.xml`
- 模型參考: `C:\odoo19\odoo-19.0\addons\product\models\product_template.py`

### 測試重點
1. 新增書籍並驗證所有欄位
2. 測試 ISBN 唯一性約束
3. 測試數量驗證（非負、可借閱 <= 總數）
4. 測試權限控制（一般使用者 vs 管理員）
5. 測試搜尋和過濾功能
6. 測試視圖在不同解析度下的顯示

