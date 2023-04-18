from odoo import api, fields, models, _
from datetime import date


class PatientTag(models.Model):
    _name = "patient.tag"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Tag"

    name = fields.Char(string='name', required=True)
    active = fields.Boolean(default=True, string='Active')
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')
    sequence = fields.Integer(string='Sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        return super(PatientTag, self).copy(default)

    # sql constraints
    _sql_constraints = [
        # Partial constraint, complemented by unique index (see below). Still
        # useful to keep because it provides a proper error message when a
        # violation occurs, as it shares the same prefix as the unique index.
        ('name_model_uid_unique', 'unique (name)', 'Filter names must be unique'),
        ('check-sequence', 'check (sequence>0)', 'Sequence must be non zero positive'),
    ]

    # _sql_constraints = [
    #     ('unique_tag_name', 'unique (name,color,color_2)', 'Name must be Unique')
    # ]
