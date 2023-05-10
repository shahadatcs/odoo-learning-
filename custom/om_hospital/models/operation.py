<<<<<<< HEAD
from odoo import api, fields, models
=======
from odoo import api, fields, models, _
>>>>>>> fdb342f4bee078528f0a037b254f5d3cedfbfc51


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Operation"
<<<<<<< HEAD
    # _rec_name = 'operation_name'
    _log_access = False
    _order = 'sequence, id'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string='Name')
    reference_record = fields.Reference([('hospital.patient', 'Patient'), ('hospital.appointment', 'Appointment')],
                                        string='Record')
    sequence = fields.Integer(string='Sequence', default=10)

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
=======
    _log_access = False

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string='Name')

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]
>>>>>>> fdb342f4bee078528f0a037b254f5d3cedfbfc51
