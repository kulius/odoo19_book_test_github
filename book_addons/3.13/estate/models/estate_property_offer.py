# in estate/models/estate_property_offer.py
from odoo import api, fields, models
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc" # 新增這一行

    _check_price = models.Constraint('CHECK(price > 0)'
        ,'The offer price must be strictly positive.')

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)  # 預設有效天數 7 天
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                # 對於新記錄，使用當前日期；對於已存在的記錄，使用 create_date
                if record.create_date:
                    # create_date 是 Datetime 類型，轉換為 Date
                    create_date = record.create_date.date() if isinstance(record.create_date, datetime) else record.create_date
                else:
                    create_date = fields.Date.today()
                delta = record.date_deadline - create_date
                record.validity = delta.days

    def action_accept_offer(self):
        for record in self:
            # 檢查是否已有其他報價被接受
            accepted_offers = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError("Another offer has already been accepted for this property.")

            record.status = 'accepted'
            # 更新對應房產的欄位
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        # vals_list 是一個字典列表，需要遍歷每個字典
        for vals in vals_list:
            # 透過 self.env 取得房產物件
            prop = self.env["estate.property"].browse(vals["property_id"])

            # 檢查新報價是否低於現有報價
            if prop.offer_ids:
                max_offer = max(prop.offer_ids.mapped('price'))
                if vals['price'] < max_offer:
                    raise UserError(f"The offer must be higher than the current best offer of {max_offer}.")

            # 更新房產狀態
            prop.state = 'offer_received'

        # 呼叫 super() 繼續執行建立流程
        return super().create(vals_list)
