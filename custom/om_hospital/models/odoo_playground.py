from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


# create a database table
class OdooPlayground(models.Model):
    _name = "odoo.playground"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Odoo Playground"

    variable = '''# Lorem Ipsum  simply dummy text
    #  of the printing and typesetting industry. 
    #  It was popularised  the 1960s with the 
    #  release of  sheets containing Lorem Ipsum passages.'''
    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code', default=variable)
    result = fields.Text(string='Result')

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
                self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)
