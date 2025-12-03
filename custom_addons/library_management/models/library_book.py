# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    """圖書資訊模型
    
    管理圖書館的書籍資訊，包括基本資訊、分類、庫存等。
    """
    _name = "library.book"
    _description = "Library Book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name, id desc"
    
    # 基本資訊
    name = fields.Char(
        string="書名",
        required=True,
        index=True,
        tracking=True,
        help="書籍的完整名稱"
    )
    isbn = fields.Char(
        string="ISBN",
        required=True,
        size=17,  # 支援連字號的 ISBN-13: 978-0-123456-78-9
        index=True,
        copy=False,
        tracking=True,
        help="國際標準書號（ISBN-10 或 ISBN-13）"
    )
    author = fields.Char(
        string="作者",
        required=True,
        index=True,
        tracking=True,
        help="書籍作者姓名"
    )
    publisher = fields.Char(
        string="出版社",
        tracking=True,
        help="出版社名稱"
    )
    publish_date = fields.Date(
        string="出版日期",
        tracking=True,
        help="書籍出版日期"
    )
    
    # 分類和庫存
    category_id = fields.Many2one(
        comodel_name='library.book.category',
        string="分類",
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
        domain="[('active', '=', True)]",
        help="書籍所屬分類"
    )
    quantity = fields.Integer(
        string="總數量",
        required=True,
        default=1,
        tracking=True,
        help="館藏總數量"
    )
    available_quantity = fields.Integer(
        string="可借閱數量",
        required=True,
        default=1,
        tracking=True,
        help="目前可供借閱的數量"
    )
    
    # 額外資訊
    description = fields.Text(
        string="簡介",
        help="書籍內容簡介"
    )
    cover_image = fields.Image(
        string="封面圖片",
        max_width=1024,
        max_height=1024,
        help="書籍封面圖片"
    )
    pages = fields.Integer(
        string="頁數",
        help="書籍總頁數"
    )
    language = fields.Selection(
        selection=[
            ('zh_TW', '繁體中文'),
            ('zh_CN', '簡體中文'),
            ('en', 'English'),
            ('ja', '日本語'),
            ('other', '其他'),
        ],
        string="語言",
        default='zh_TW',
        help="書籍語言"
    )
    
    # 計算欄位
    is_available = fields.Boolean(
        string="可借閱",
        compute='_compute_is_available',
        store=True,
        help="是否有可借閱的庫存"
    )
    
    # 系統欄位
    active = fields.Boolean(
        string="啟用",
        default=True,
        help="取消勾選以停用此書籍（不會刪除資料）"
    )
    
    # SQL 約束 - Odoo 19 新語法
    _unique_isbn = models.Constraint(
        'UNIQUE(isbn)',
        'ISBN 必須唯一！此 ISBN 已存在於系統中。'
    )
    
    _check_quantity = models.Constraint(
        'CHECK(quantity >= 0)',
        '總數量必須為非負整數！'
    )
    
    _check_available_quantity = models.Constraint(
        'CHECK(available_quantity >= 0)',
        '可借閱數量必須為非負整數！'
    )
    
    @api.depends('available_quantity')
    def _compute_is_available(self):
        """計算是否可借閱"""
        for record in self:
            record.is_available = record.available_quantity > 0
    
    @api.constrains('isbn')
    def _check_isbn_format(self):
        """驗證 ISBN 格式（ISBN-10 或 ISBN-13）"""
        for record in self:
            if not record.isbn:
                continue
            
            # 移除連字號和空格
            isbn_clean = re.sub(r'[\s-]', '', record.isbn)
            
            # 檢查是否為純數字（允許 ISBN-10 最後一位為 X）
            if not re.match(r'^\d{9}[\dX]$|^\d{13}$', isbn_clean):
                raise ValidationError(
                    f'ISBN 格式不正確！\n'
                    f'請輸入有效的 ISBN-10（10位數字）或 ISBN-13（13位數字）。\n'
                    f'範例：978-0-123456-78-9 或 0-123456-78-9'
                )
    
    @api.constrains('available_quantity', 'quantity')
    def _check_available_quantity_limit(self):
        """驗證可借閱數量不超過總數量"""
        for record in self:
            if record.available_quantity > record.quantity:
                raise ValidationError(
                    f'可借閱數量（{record.available_quantity}）不能大於總數量（{record.quantity}）！'
                )
    
    @api.constrains('pages')
    def _check_pages_positive(self):
        """驗證頁數為正數"""
        for record in self:
            if record.pages and record.pages <= 0:
                raise ValidationError('頁數必須為正整數！')
    
    # 借閱相關欄位
    borrowing_ids = fields.One2many(
        comodel_name='library.borrowing',
        inverse_name='book_id',
        string="借閱記錄",
        copy=False,
        help="此書籍的所有借閱記錄"
    )
    
    current_borrowing_id = fields.Many2one(
        comodel_name='library.borrowing',
        string="當前借閱",
        compute='_compute_current_borrowing',
        store=True,
        help="當前借閱中的記錄"
    )
    
    borrowed_count = fields.Integer(
        string="總借閱次數",
        compute='_compute_borrowed_count',
        store=True,
        help="此書籍被借閱的總次數（不包括草稿和已取消）"
    )
    
    @api.depends('borrowing_ids', 'borrowing_ids.state')
    def _compute_current_borrowing(self):
        """計算當前借閱記錄"""
        for record in self:
            current = record.borrowing_ids.filtered(lambda b: b.state == 'borrowed')
            record.current_borrowing_id = current[0] if current else False
    
    @api.depends('borrowing_ids', 'borrowing_ids.state')
    def _compute_borrowed_count(self):
        """計算總借閱次數"""
        for record in self:
            record.borrowed_count = len(record.borrowing_ids.filtered(
                lambda b: b.state in ['borrowed', 'returned']
            ))
    
    def action_quick_borrow(self):
        """快速借閱按鈕動作"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': '快速借閱',
            'res_model': 'library.borrowing',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_id': self.id,
                'default_borrow_date': fields.Date.today(),
            }
        }
    
    def action_view_borrowings(self):
        """查看借閱記錄動作"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} - 借閱記錄',
            'res_model': 'library.borrowing',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id}
        }

