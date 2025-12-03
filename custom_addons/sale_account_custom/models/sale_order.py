# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 運送備註欄位
    shipping_note = fields.Text(
        string='運送備註',
        help='記錄運送相關的特殊說明或注意事項',
        copy=False,
        tracking=True
    )

    # 會計應收總金額
    total_invoice_amount = fields.Monetary(
        string='應收帳款總金額',
        compute='_compute_total_invoice_amount',
        store=True,
        currency_field='currency_id',
        help='此銷售訂單已開立的會計應收總金額'
    )

    @api.depends('invoice_ids', 'invoice_ids.amount_total', 'invoice_ids.state')
    def _compute_total_invoice_amount(self):
        """計算已開立的會計應收總金額（不包含已取消的發票）"""
        for order in self:
            # 只計算非取消狀態的發票
            invoices = order.invoice_ids.filtered(lambda inv: inv.state != 'cancel')
            order.total_invoice_amount = sum(invoices.mapped('amount_total'))

