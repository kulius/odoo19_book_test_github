# Change: 新增圖書館借閱管理功能

## Why
目前圖書館管理系統只能管理書籍的基本資訊和庫存，但缺乏核心的借閱管理功能。圖書管理員需要能夠記錄書籍的借出、歸還和續借，並自動更新庫存狀態，以實時追蹤每本書的流通情況。這是圖書館管理系統的核心業務流程，是連接書籍資訊和讀者服務的關鍵功能。

沒有借閱管理功能，圖書管理員無法：
- 追蹤哪些書被誰借走
- 知道書籍何時應該歸還
- 管理逾期書籍
- 統計借閱頻率和熱門書籍

## What Changes
- 建立新的 `library.borrowing` 模型，記錄借閱記錄
  - 包含借閱者、書籍、借閱日期、到期日、歸還日期、狀態等資訊
  - 支援借閱、歸還、續借三種主要操作
  - 自動計算到期日和逾期天數
  
- 擴展現有的 `library.book` 模型
  - 添加 `borrowing_ids` One2many 欄位，連結借閱記錄
  - 添加 `current_borrowing_id` Many2one 欄位，指向當前借閱記錄
  - 添加 `borrowed_count` 計算欄位，統計總借閱次數
  - 修改 `available_quantity` 的計算邏輯，根據借閱狀態自動更新

- 建立完整的使用者介面
  - 借閱記錄的列表、表單、搜尋視圖
  - 在書籍表單中顯示借閱歷史
  - 提供快速借閱、歸還、續借的按鈕
  - 看板視圖依狀態分組（借閱中、已歸還、逾期）

- 實作業務邏輯和驗證
  - 借閱時檢查庫存是否足夠
  - 借閱時自動扣減可借閱數量
  - 歸還時自動增加可借閱數量
  - 續借時檢查續借次數限制
  - 逾期檢查和提醒

- 設定權限控制
  - 一般使用者可查看自己的借閱記錄
  - 圖書管理員可管理所有借閱記錄
  - 記錄規則確保資料安全

- 新增初始資料
  - 借閱設定（預設借閱天數、最大續借次數等）

## Impact
- **新增的規格**: `library-borrowing-management` - 圖書借閱管理能力
- **修改的規格**: `library-book-management` - 擴展庫存追蹤邏輯
- **影響的程式碼**: 
  - 新增 `models/library_borrowing.py` - 借閱模型
  - 修改 `models/library_book.py` - 添加借閱相關欄位和方法
  - 新增 `views/library_borrowing_views.xml` - 借閱視圖
  - 修改 `views/library_book_views.xml` - 添加借閱相關按鈕和欄位
  - 修改 `views/library_menus.xml` - 添加借閱選單
  - 修改 `security/library_security.xml` - 添加借閱記錄規則
  - 修改 `security/ir.model.access.csv` - 添加借閱模型權限
  - 新增 `data/library_borrowing_config_data.xml` - 借閱設定資料
- **依賴模組**: `base`, `mail`, `library_management`
- **資料庫影響**: 新增資料表 `library_borrowing`，修改 `library_book` 的計算邏輯

## System Architecture Context
此變更是圖書館管理系統的第二階段，建立在第一階段（圖書資訊管理）的基礎上：
1. ✅ **圖書資訊管理**（已完成）
2. 🔄 **借閱管理**（本次變更）
3. 📋 讀者管理（未來變更 - 可選，目前使用 res.partner）
4. 📋 進階查詢和報表（未來變更）
5. 📋 預約和排隊功能（未來變更）

## User Story
**作為一名圖書管理員**，我希望能管理書籍的借閱、歸還和續借記錄，並自動更新庫存狀態，以實時追蹤每本書的流通情況。

**驗收標準**：
- 能夠記錄書籍借出，選擇借閱者和書籍
- 借閱時自動扣減可借閱數量
- 能夠記錄書籍歸還，自動增加可借閱數量
- 能夠處理續借請求，延長到期日
- 系統自動計算到期日和逾期天數
- 能夠查看所有借閱記錄，包括借閱中和已歸還
- 能夠過濾逾期的借閱記錄
- 在書籍詳細資訊中查看借閱歷史
- 系統自動追蹤庫存變化

## Dependencies and Constraints
- 依賴已完成的 `library_management` 模組
- 使用 Odoo 標準的 `res.partner` 模型作為借閱者
- 遵守 Odoo 19 開發規範
- 參考 Odoo 原始碼（特別是 `sale` 和 `stock` 模組）的狀態管理模式

