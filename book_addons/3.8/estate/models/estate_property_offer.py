# in estate/models/estate_property_offer.py
from odoo import api, fields, models
from datetime import timedelta, datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

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

