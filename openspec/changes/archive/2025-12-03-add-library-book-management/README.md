# 圖書館管理系統 - 圖書資訊管理

## 📋 提案概述

這是圖書館管理系統的第一個核心功能模組，實作完整的圖書資訊管理能力。

**變更 ID**: `add-library-book-management`  
**狀態**: 待審核 (Pending Review)  
**類型**: 新功能 (New Feature)

## 🎯 目標

為學校圖書館建立數位化的圖書管理系統，取代傳統手工記錄方式。本次變更專注於圖書資訊管理的核心功能。

## 📦 交付內容

### 新增模組
- **模組名稱**: `library_management`
- **位置**: `custom_addons/library_management/`
- **依賴**: `base`, `mail`

### 資料模型
1. **library.book** - 圖書資訊
   - 基本資訊：書名、ISBN、作者、出版社、出版日期
   - 分類和庫存：分類、總數量、可借閱數量
   - 額外資訊：簡介、封面圖片、頁數、語言
   - 計算欄位：可借閱狀態

2. **library.book.category** - 圖書分類
   - 分類名稱、代碼、描述
   - 書籍數量統計

### 使用者介面
- ✅ 列表視圖 (List View) - 快速瀏覽書籍
- ✅ 表單視圖 (Form View) - 詳細資訊編輯
- ✅ 看板視圖 (Kanban View) - 視覺化卡片顯示
- ✅ 搜尋視圖 (Search View) - 多維度查詢

### 功能特性
- ✅ 完整的 CRUD 操作
- ✅ ISBN 格式驗證和唯一性檢查
- ✅ 庫存數量追蹤和驗證
- ✅ 多維度搜尋和過濾
- ✅ 訊息追蹤 (Chatter)
- ✅ 權限控制（管理員 vs 一般使用者）
- ✅ 預設分類資料

## 📚 文件結構

```
add-library-book-management/
├── proposal.md          # 提案說明（為什麼、改什麼、影響）
├── tasks.md            # 實作任務清單（9 大階段、45+ 子任務）
├── design.md           # 技術設計文件（架構、決策、權衡）
├── specs/
│   └── library-book-management/
│       └── spec.md     # 功能規格（10 個需求、50+ 場景）
└── README.md           # 本文件
```

## 🔍 關鍵需求

### 1. 圖書基本資訊管理
- 新增、編輯、刪除書籍
- ISBN 驗證和唯一性檢查
- 權限控制

### 2. 圖書分類管理
- 建立和維護分類體系
- 分類代碼唯一性
- 停用/啟用分類

### 3. 圖書庫存追蹤
- 總數量和可借閱數量
- 自動計算可借閱狀態
- 數量驗證規則

### 4. 圖書資訊查詢
- 書名、作者、ISBN 搜尋
- 分類過濾
- 庫存狀態過濾

### 5. 多視圖顯示
- 列表、表單、看板視圖
- 視覺化庫存狀態
- 響應式佈局

### 6. 資料驗證
- 必填欄位檢查
- ISBN 格式驗證
- 數量範圍驗證

### 7. 訊息追蹤
- 變更記錄
- 訊息和註記
- 活動提醒

### 8. 權限控制
- Library Manager（完整權限）
- Library User（唯讀權限）

### 9. 預設資料
- 預設圖書分類
- 可修改和擴展

## 🚀 下一步

### 審核階段
1. **閱讀提案**: 查看 `proposal.md` 了解變更的原因和影響
2. **檢視設計**: 閱讀 `design.md` 了解技術決策和架構
3. **審查規格**: 查看 `specs/library-book-management/spec.md` 了解詳細需求
4. **評估任務**: 檢視 `tasks.md` 了解實作計畫

### 批准後
執行以下命令開始實作：
```bash
# 開始實作（由 AI 助手執行）
# 助手會依照 tasks.md 逐步完成所有任務
```

### 完成後
執行以下命令歸檔變更：
```bash
openspec archive add-library-book-management
```

## 📊 規格統計

- **需求數量**: 10 個主要需求
- **場景數量**: 50+ 個測試場景
- **任務數量**: 45+ 個實作任務
- **預估工時**: 2-3 天（包含測試和文件）

## 🔗 相關連結

### 參考文件
- [Odoo 19 官方文件](https://www.odoo.com/documentation/19.0/)
- [Odoo Python 編碼指南](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html)
- [專案治理層規範](../../project.md)

### 參考模組
- `C:\odoo19\odoo-19.0\addons\sale` - 視圖結構參考
- `C:\odoo19\odoo-19.0\addons\account` - 表單設計參考
- `C:\odoo19\odoo-19.0\addons\product` - 模型設計參考

## ⚠️ 重要注意事項

### 實作前必讀
1. ✅ 已讀取 `openspec/project.md`（專案規範）
2. ✅ 已讀取 `openspec/AGENTS.md`（OpenSpec 工作流程）
3. ⚠️ 實作視圖前必須讀取 Odoo 原始碼參考
4. ⚠️ 繼承視圖時必須生成精確的 XPath
5. ⚠️ 必須遵守 Odoo 19 命名規範
6. ⚠️ 必須使用 Odoo 19 新語法（`models.Constraint`, `fields.Command`）

### 驗證檢查
- ✅ `openspec validate add-library-book-management --strict` 已通過
- ⏳ 程式碼實作後需執行 Odoo 功能測試
- ⏳ 需驗證權限控制正確性
- ⏳ 需驗證資料驗證規則

## 📝 變更歷史

- **2024-12-03**: 建立初始提案
  - 完成 proposal.md
  - 完成 tasks.md（9 階段、45+ 任務）
  - 完成 design.md（完整技術設計）
  - 完成 spec.md（10 需求、50+ 場景）
  - 通過嚴格驗證

## 👥 利益相關者

- **圖書管理員**: 主要使用者，負責管理書籍資料
- **讀者**: 次要使用者，查詢書籍資訊（未來功能）
- **系統管理員**: 負責模組安裝和權限配置

## 🎓 學習資源

如果您是第一次接觸 Odoo 開發，建議先查看：
1. `C:\odoo19\book_addons\` - 包含 estate 模組的演進範例
2. Odoo 官方教學文件
3. 專案治理層規範（`openspec/project.md`）

---

**準備好了嗎？** 請審核此提案，批准後即可開始實作！ 🚀

