# Implementation Tasks

## 1. 模型設計和實作
- [ ] 1.1 建立 `models/library_borrowing.py` 模型檔案
- [ ] 1.2 定義 `library.borrowing` 模型基本欄位
  - [ ] 1.2.1 借閱者欄位 (partner_id: Many2one → res.partner)
  - [ ] 1.2.2 書籍欄位 (book_id: Many2one → library.book)
  - [ ] 1.2.3 日期欄位 (borrow_date, due_date, return_date)
  - [ ] 1.2.4 狀態欄位 (state: Selection)
  - [ ] 1.2.5 續借次數欄位 (renew_count: Integer)
- [ ] 1.3 定義計算欄位
  - [ ] 1.3.1 逾期天數 (overdue_days: Integer, computed)
  - [ ] 1.3.2 是否逾期 (is_overdue: Boolean, computed)
  - [ ] 1.3.3 可否續借 (can_renew: Boolean, computed)
- [ ] 1.4 實作約束條件
  - [ ] 1.4.1 SQL 約束：歸還日期不能早於借閱日期
  - [ ] 1.4.2 Python 約束：檢查書籍庫存
  - [ ] 1.4.3 Python 約束：檢查續借次數限制
- [ ] 1.5 繼承 mail.thread 和 mail.activity.mixin
- [ ] 1.6 設定 _order 預設排序

## 2. 業務邏輯實作
- [ ] 2.1 實作借閱動作 (action_borrow)
  - [ ] 2.1.1 檢查書籍可借閱數量
  - [ ] 2.1.2 扣減書籍可借閱數量
  - [ ] 2.1.3 設定狀態為「借閱中」
  - [ ] 2.1.4 計算到期日
  - [ ] 2.1.5 記錄訊息到 Chatter
- [ ] 2.2 實作歸還動作 (action_return)
  - [ ] 2.2.1 增加書籍可借閱數量
  - [ ] 2.2.2 設定歸還日期
  - [ ] 2.2.3 設定狀態為「已歸還」
  - [ ] 2.2.4 記錄訊息到 Chatter
- [ ] 2.3 實作續借動作 (action_renew)
  - [ ] 2.3.1 檢查續借次數限制
  - [ ] 2.3.2 檢查是否已歸還
  - [ ] 2.3.3 延長到期日
  - [ ] 2.3.4 增加續借次數
  - [ ] 2.3.5 記錄訊息到 Chatter
- [ ] 2.4 實作取消動作 (action_cancel)
  - [ ] 2.4.1 恢復書籍可借閱數量（如尚未歸還）
  - [ ] 2.4.2 設定狀態為「已取消」
- [ ] 2.5 覆寫 create 方法
  - [ ] 2.5.1 自動設定借閱日期為今天
  - [ ] 2.5.2 自動計算到期日
  - [ ] 2.5.3 自動設定狀態為「草稿」

## 3. 擴展書籍模型
- [ ] 3.1 修改 `models/library_book.py`
- [ ] 3.2 添加 One2many 欄位 (borrowing_ids)
- [ ] 3.3 添加 Many2one 欄位 (current_borrowing_id)
- [ ] 3.4 添加計算欄位 (borrowed_count)
- [ ] 3.5 修改 available_quantity 的計算邏輯（改為手動管理）
- [ ] 3.6 添加快速借閱按鈕方法 (action_quick_borrow)

## 4. 視圖實作 - 借閱記錄
- [ ] 4.1 建立 `views/library_borrowing_views.xml`
- [ ] 4.2 實作列表視圖 (list view)
  - [ ] 4.2.1 顯示關鍵欄位
  - [ ] 4.2.2 使用 decoration 標示逾期記錄
  - [ ] 4.2.3 設定 sample="1"
- [ ] 4.3 實作表單視圖 (form view)
  - [ ] 4.3.1 參考 sale.order 的表單結構
  - [ ] 4.3.2 建立 header 區域（狀態列、按鈕）
  - [ ] 4.3.3 建立 sheet 區域
  - [ ] 4.3.4 使用 group 佈局分組顯示欄位
  - [ ] 4.3.5 加入 chatter
- [ ] 4.4 實作搜尋視圖 (search view)
  - [ ] 4.4.1 可搜尋欄位：借閱者、書籍
  - [ ] 4.4.2 過濾器：借閱中、已歸還、逾期
  - [ ] 4.4.3 群組依據：借閱者、書籍、狀態
- [ ] 4.5 實作看板視圖 (kanban view)
  - [ ] 4.5.1 參考 Odoo 原始碼設計卡片佈局
  - [ ] 4.5.2 顯示借閱者、書籍、到期日
  - [ ] 4.5.3 設定預設分組（依狀態）

## 5. 視圖實作 - 擴展書籍視圖
- [ ] 5.1 修改 `views/library_book_views.xml`
- [ ] 5.2 在表單視圖添加借閱歷史分頁
  - [ ] 5.2.1 使用 One2many 欄位顯示借閱記錄
  - [ ] 5.2.2 添加內嵌列表視圖
- [ ] 5.3 在表單視圖添加統計按鈕
  - [ ] 5.3.1 顯示總借閱次數
  - [ ] 5.3.2 點擊可查看借閱記錄列表
- [ ] 5.4 在表單視圖添加快速借閱按鈕
  - [ ] 5.4.1 只在有庫存時顯示
  - [ ] 5.4.2 點擊開啟借閱表單
- [ ] 5.5 在列表視圖添加借閱狀態指示

## 6. 動作和選單
- [ ] 6.1 修改 `views/library_menus.xml`
- [ ] 6.2 定義 window action：action_library_borrowing
- [ ] 6.3 定義 window action：action_library_borrowing_overdue
- [ ] 6.4 建立子選單：Borrowings（連結至 action_library_borrowing）
- [ ] 6.5 建立子選單：Overdue Borrowings（連結至 action_library_borrowing_overdue）

## 7. 安全規則
- [ ] 7.1 修改 `security/library_security.xml`
- [ ] 7.2 定義記錄規則：使用者只能看到自己的借閱記錄
- [ ] 7.3 定義記錄規則：管理員可以看到所有借閱記錄
- [ ] 7.4 修改 `security/ir.model.access.csv`
- [ ] 7.5 設定 library.borrowing 的讀取權限（所有使用者）
- [ ] 7.6 設定 library.borrowing 的寫入/建立/刪除權限（僅管理員）

## 8. 初始資料
- [ ] 8.1 建立 `data/library_borrowing_config_data.xml`
- [ ] 8.2 新增借閱設定（預設借閱天數：14 天）
- [ ] 8.3 新增借閱設定（最大續借次數：2 次）
- [ ] 8.4 新增借閱設定（續借延長天數：14 天）

## 9. 測試和驗證
- [ ] 9.1 執行 `openspec validate add-library-borrowing-management --strict`
- [ ] 9.2 在 Odoo 中安裝/更新模組並測試
- [ ] 9.3 測試借閱功能
  - [ ] 9.3.1 測試正常借閱
  - [ ] 9.3.2 測試庫存不足時的借閱
  - [ ] 9.3.3 驗證可借閱數量自動扣減
- [ ] 9.4 測試歸還功能
  - [ ] 9.4.1 測試正常歸還
  - [ ] 9.4.2 驗證可借閱數量自動增加
  - [ ] 9.4.3 驗證歸還日期記錄
- [ ] 9.5 測試續借功能
  - [ ] 9.5.1 測試正常續借
  - [ ] 9.5.2 測試超過續借次數限制
  - [ ] 9.5.3 驗證到期日延長
- [ ] 9.6 測試逾期檢查
  - [ ] 9.6.1 驗證逾期天數計算
  - [ ] 9.6.2 驗證逾期記錄標示
- [ ] 9.7 測試權限控制
  - [ ] 9.7.1 一般使用者只能看到自己的借閱記錄
  - [ ] 9.7.2 管理員可以管理所有借閱記錄
- [ ] 9.8 測試搜尋和過濾功能
- [ ] 9.9 測試視圖在不同裝置上的顯示效果

## 10. 文件和完成
- [ ] 10.1 在模型中加入適當的 docstring 和註解
- [ ] 10.2 確保所有檔案符合 Odoo 編碼規範
- [ ] 10.3 更新 `__manifest__.py` 中的描述和版本資訊
- [ ] 10.4 執行最終驗證
- [ ] 10.5 準備歸檔文件

