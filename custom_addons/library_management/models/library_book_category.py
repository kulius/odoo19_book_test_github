# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LibraryBookCategory(models.Model):
    """圖書分類模型
    
    用於管理圖書館的書籍分類系統，每個分類包含唯一的代碼和名稱。
    """
    _name = "library.book.category"
    _description = "Library Book Category"
    _order = "code, name"
    
    # 基本欄位
    name = fields.Char(
        string="分類名稱",
        required=True,
        translate=True,
        help="圖書分類的名稱（支援多語言）"
    )
    code = fields.Char(
        string="分類代碼",
        required=True,
        size=10,
        help="唯一的分類代碼，用於快速識別"
    )
    description = fields.Text(
        string="描述",
        help="分類的詳細描述"
    )
    active = fields.Boolean(
        string="啟用",
        default=True,
        help="取消勾選以停用此分類（不會刪除資料）"
    )
    
    # 計算欄位
    book_count = fields.Integer(
        string="書籍數量",
        compute='_compute_book_count',
        help="此分類下的書籍總數"
    )
    
    # SQL 約束 - Odoo 19 新語法
    _unique_code = models.Constraint(
        'UNIQUE(code)',
        '分類代碼必須唯一！'
    )
    
    @api.depends('code', 'name')
    def _compute_display_name(self):
        """自訂顯示名稱：[代碼] 名稱"""
        for record in self:
            if record.code:
                record.display_name = f"[{record.code}] {record.name}"
            else:
                record.display_name = record.name
    
    def _compute_book_count(self):
        """計算此分類下的書籍數量"""
        for record in self:
            record.book_count = self.env['library.book'].search_count([
                ('category_id', '=', record.id)
            ])
    
    def name_get(self):
        """自訂顯示名稱格式"""
        result = []
        for record in self:
            if record.code:
                name = f"[{record.code}] {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result

