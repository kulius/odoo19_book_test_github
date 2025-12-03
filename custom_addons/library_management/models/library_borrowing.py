# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class LibraryBorrowing(models.Model):
    """圖書借閱記錄模型
    
    管理圖書館的借閱記錄，包括借閱、歸還、續借和逾期管理。
    """
    _name = "library.borrowing"
    _description = "Library Borrowing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "borrow_date desc, id desc"
    
    # 基本資訊
    name = fields.Char(
        string="借閱編號",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: '新建',
        help="借閱記錄的唯一編號"
    )
    
    # 關聯欄位
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="借閱者",
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
        help="借閱書籍的讀者"
    )
    
    book_id = fields.Many2one(
        comodel_name='library.book',
        string="書籍",
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
        help="被借閱的書籍"
    )
    
    # 日期欄位
    borrow_date = fields.Date(
        string="借閱日期",
        required=True,
        default=fields.Date.today,
        copy=False,
        tracking=True,
        help="書籍借出的日期"
    )
    
    due_date = fields.Date(
        string="到期日",
        required=True,
        copy=False,
        tracking=True,
        help="應歸還的日期"
    )
    
    return_date = fields.Date(
        string="歸還日期",
        copy=False,
        readonly=True,
        tracking=True,
        help="實際歸還的日期"
    )
    
    # 狀態和計數
    state = fields.Selection(
        selection=[
            ('draft', '草稿'),
            ('borrowed', '借閱中'),
            ('returned', '已歸還'),
            ('cancelled', '已取消'),
        ],
        string='狀態',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
        help="借閱記錄的當前狀態"
    )
    
    renew_count = fields.Integer(
        string="續借次數",
        default=0,
        copy=False,
        tracking=True,
        help="已續借的次數"
    )
    
    # 計算欄位
    overdue_days = fields.Integer(
        string="逾期天數",
        compute='_compute_overdue_days',
        store=True,
        help="逾期的天數（0 表示未逾期）"
    )
    
    is_overdue = fields.Boolean(
        string="是否逾期",
        compute='_compute_overdue_days',
        store=True,
        help="標記是否逾期"
    )
    
    can_renew = fields.Boolean(
        string="可否續借",
        compute='_compute_can_renew',
        help="是否可以續借"
    )
    
    # 配置參數（可從系統參數讀取，這裡先硬編碼）
    max_renew_count = fields.Integer(
        string="最大續借次數",
        default=2,
        help="允許的最大續借次數"
    )
    
    # SQL 約束 - Odoo 19 新語法
    _check_return_date = models.Constraint(
        'CHECK(return_date IS NULL OR return_date >= borrow_date)',
        '歸還日期不能早於借閱日期！'
    )
    
    @api.depends('due_date', 'return_date', 'state')
    def _compute_overdue_days(self):
        """計算逾期天數"""
        today = fields.Date.today()
        for record in self:
            if record.state == 'borrowed':
                # 借閱中：與今天比較
                if record.due_date and record.due_date < today:
                    delta = today - record.due_date
                    record.overdue_days = delta.days
                    record.is_overdue = True
                else:
                    record.overdue_days = 0
                    record.is_overdue = False
            elif record.state == 'returned' and record.return_date:
                # 已歸還：與歸還日期比較
                if record.due_date and record.return_date > record.due_date:
                    delta = record.return_date - record.due_date
                    record.overdue_days = delta.days
                    record.is_overdue = True
                else:
                    record.overdue_days = 0
                    record.is_overdue = False
            else:
                record.overdue_days = 0
                record.is_overdue = False
    
    @api.depends('state', 'renew_count', 'max_renew_count')
    def _compute_can_renew(self):
        """計算是否可以續借"""
        for record in self:
            record.can_renew = (
                record.state == 'borrowed' and 
                record.renew_count < record.max_renew_count
            )
    
    @api.model_create_multi
    def create(self, vals_list):
        """建立借閱記錄時自動生成編號和計算到期日"""
        for vals in vals_list:
            # 生成借閱編號
            if vals.get('name', '新建') == '新建':
                vals['name'] = self.env['ir.sequence'].next_by_code('library.borrowing') or '新建'
            
            # 自動計算到期日（如果沒有提供）
            if 'due_date' not in vals and 'borrow_date' in vals:
                borrow_date = fields.Date.from_string(vals['borrow_date'])
                vals['due_date'] = borrow_date + timedelta(days=14)  # 預設 14 天
        
        return super().create(vals_list)
    
    def action_borrow(self):
        """執行借閱操作"""
        for record in self:
            # 檢查狀態
            if record.state != 'draft':
                raise UserError('只能借閱草稿狀態的記錄！')
            
            # 檢查書籍庫存
            if record.book_id.available_quantity <= 0:
                raise UserError(f'書籍「{record.book_id.name}」庫存不足，無法借閱！')
            
            # 扣減庫存
            record.book_id.available_quantity -= 1
            
            # 更新狀態
            record.state = 'borrowed'
            
            # 記錄訊息
            record.message_post(
                body=f'書籍已借出給 {record.partner_id.name}，到期日：{record.due_date}',
                subject='借閱成功'
            )
        
        return True
    
    def action_return(self):
        """執行歸還操作"""
        for record in self:
            # 檢查狀態
            if record.state != 'borrowed':
                raise UserError('只能歸還借閱中的記錄！')
            
            # 增加庫存
            record.book_id.available_quantity += 1
            
            # 記錄歸還日期
            record.return_date = fields.Date.today()
            
            # 更新狀態
            record.state = 'returned'
            
            # 記錄訊息
            message = f'{record.partner_id.name} 已歸還書籍'
            if record.is_overdue:
                message += f'（逾期 {record.overdue_days} 天）'
            record.message_post(
                body=message,
                subject='歸還成功'
            )
        
        return True
    
    def action_renew(self):
        """執行續借操作"""
        for record in self:
            # 檢查狀態
            if record.state != 'borrowed':
                raise UserError('只能續借借閱中的記錄！')
            
            # 檢查續借次數
            if record.renew_count >= record.max_renew_count:
                raise UserError(f'已達最大續借次數（{record.max_renew_count} 次）！')
            
            # 延長到期日
            old_due_date = record.due_date
            record.due_date = record.due_date + timedelta(days=14)  # 延長 14 天
            record.renew_count += 1
            
            # 記錄訊息
            record.message_post(
                body=f'續借成功！到期日從 {old_due_date} 延長至 {record.due_date}（第 {record.renew_count} 次續借）',
                subject='續借成功'
            )
        
        return True
    
    def action_cancel(self):
        """取消借閱操作"""
        for record in self:
            # 檢查狀態
            if record.state == 'returned':
                raise UserError('無法取消已歸還的借閱！')
            
            # 如果是借閱中，需要恢復庫存
            if record.state == 'borrowed':
                record.book_id.available_quantity += 1
            
            # 更新狀態
            record.state = 'cancelled'
            
            # 記錄訊息
            record.message_post(
                body=f'借閱記錄已取消',
                subject='借閱取消'
            )
        
        return True
    
    @api.constrains('book_id', 'state')
    def _check_book_availability(self):
        """檢查書籍可借閱性（在建立或修改時）"""
        for record in self:
            if record.state == 'draft' and record.book_id:
                # 草稿狀態時只是警告，不阻止
                if record.book_id.available_quantity <= 0:
                    # 這裡不拋出異常，因為可能是預先建立記錄
                    pass
    
    def name_get(self):
        """自訂顯示名稱"""
        result = []
        for record in self:
            name = f"{record.name} - {record.partner_id.name} / {record.book_id.name}"
            result.append((record.id, name))
        return result

