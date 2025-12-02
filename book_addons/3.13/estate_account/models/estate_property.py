 # in estate_account/models/estate_property.py
from odoo import models, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        print("Creating invoice with lines...")
        for prop in self:
            # 建立發票
            self.env['account.move'].create({
                'partner_id': prop.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': prop.name, # 品項名稱就是房產名稱
                        'quantity': 1.0,
                        'price_unit': prop.selling_price * 0.06
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1.0,
                        'price_unit': 100.0
                    })
                ]
            })

        return super().action_set_sold()