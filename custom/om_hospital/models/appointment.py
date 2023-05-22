from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta
from random import randrange
import random


# create a database table
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'ref'
    _order = 'id desc'

    name = fields.Char(string='Sequence', default='New')
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='patient', ondelete='cascade')
    gender = fields.Selection(related='patient_id.gender')  # readonly=false that selection progress
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='reference', help='reference of the patient from the patient record')
    # patient_id = fields.Many2one(comodel_name='hospital.patient', string='patient')
    # Define HTML Field In Odoo
    prescription = fields.Html(string='Prescription')
    operation = fields.Char(string='Operation')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    # Add Statusbar In Odoo Development
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled'),
         ('warning', 'Warning')],
        default='draft', string="Status", required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy')
    hide_sales_price = fields.Boolean(string='Hide sales price')
    operation_id = fields.Many2one('hospital.operation', string="Operations")
    progress = fields.Integer(string='Progress', compute='compute_progress')
    # progress_gauge = fields.Integer(string='Progress', compute='compute_progress')
    duration = fields.Float(string='Duration')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    amount_total = fields.Monetary(string='Total', compute='compute_total_price', currency_field='currency_id')

    @api.depends('pharmacy_lines_ids')
    def compute_total_price(self):
        for rec in self:
            amount_total = 0
            for line in rec.pharmacy_lines_ids:
                amount_total += line.price_subtotal
        rec.amount_total = amount_total

    def set_line_number(self):
        sl_no = 0
        for line in self.pharmacy_lines_ids:
            sl_no += 1
            line.sl_no = sl_no
        return

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        res.set_line_number()
        return res

    def write(self, values):
        res = super(HospitalAppointment, self).write(values)
        self.set_line_number()
        return res

    # Define Onchange Functions
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_notification(self):
        message = 'Button Click on Successful'
        action = self.env.ref('om_hospital.action_hospital_appointment')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                # 'message': message,
                'type': 'success',
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient',
                }],
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')]
                }
            }
        }

    def unlink(self):
        print("test__________")
        if self.state != 'draft':
            raise ValidationError(_('you cannot delete appointment with Draft status'))
        return super(HospitalAppointment, self).unlink()

    def action_test(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.hackerrank.com/',
        }

    # print('click button')
    # # Rainbow Effect
    # return {
    #     'effect': {
    #         'fadeout': 'slow',
    #         'message': 'Click Successful',
    #         'type': 'rainbow_man',
    #     }
    # }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successful',
                'type': 'rainbow_man',
            }
        }

    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_warning(self):
        for rec in self:
            rec.state = 'warning'

    @api.depends('state')
    def compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(0, 30)
            elif rec.state == 'done':
                progress = random.randrange(0, 20)
            elif rec.state == 'cancel':
                progress = random.randrange(0, 15)
            elif rec.state == 'warning':
                progress = 10
            else:
                progress = 0
            rec.progress = progress

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         operation = rec.operation
    #         result.append(operation)
    #     return result

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_('Missing Phone Number in Patient Record'))
        message = 'Hi *%s*, your *appointment* number is: %s, Thank you' % (self.patient_id.name, self.name)
        whatsapp_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (self.patient_id.phone, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_send_email(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                email_values = {
                    'subject': 'Test'
                }
                template.send_mail(rec.id, force_send=True, email_values=email_values)

    class AppointmentPharmacyLines(models.Model):
        _name = "appointment.pharmacy.lines"
        _description = "Appointment Pharmacy Lines"

        sl_no = fields.Integer(string='SNO.')
        product_id = fields.Many2one('product.product', required=True)
        price_unit = fields.Float(related='product_id.list_price', digits='Product Price')
        qty = fields.Integer(string='Quantity', default=1)
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
        currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
        price_subtotal = fields.Monetary(string='Subtotal', compute='compute_price_subtotal',
                                         currency_field='currency_id')

        @api.onchange('product_id')
        def onchange_product_id(self):
            self.price_unit = self.product_id.lst_price

        @api.depends('price_unit', 'qty')
        def compute_price_subtotal(self):
            for rec in self:
                rec.price_subtotal = rec.price_unit * rec.qty
