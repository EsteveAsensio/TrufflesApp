from odoo import models, fields, api

class Invoice(models.Model):
    _name = 'trufflesapp.invoice'
    _description = 'The invoice about the products'

    name=fields.Integer(string="References", required=True, default=lambda self: self.setReferences()) #ID Autoincrementable
    description=fields.Html(string="Description", help="Description of the Invoice")
    dateInvoice=fields.Datetime(string="Date",help="The date of the invoice", required=True, default=fields.Datetime.now)
    base=fields.Float(string="Base", help="The total price of the invoice without IVA", compute="setPriceBase", store=True)
    iva=fields.Selection(string="IVA", selection=[('0','0%'), ('10','10%'), ('21','21%')], default="0")
    totalIva=fields.Float(string="TotalIVA", help="The total price of the invoice with IVA", compute="computeTotalIVA",store=True)
    state=fields.Selection(string="State", selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed')], default="Draft")
    lines=fields.One2many("trufflesapp.lines", "invoiceid") #linea (nuevo modelo)
    customer=fields.Many2one("res.partner", string="Customer", required=True) #Relacion a modelo customers
    active=fields.Boolean(string="Is active",default=True)

    def init(self):
        self.setPriceBase()

    def setReferences(self):
        result = self.env['trufflesapp.invoice'].search_read()
        if len(result) == 0:
            return 1
        else:
           return result[-1]["name"] +1
        
    @api.depends("lines")
    def setPriceBase(self):
        self.base = 0.0
        newPrice = 0.0
        for line in self.lines:
            newPrice = newPrice + line.totalprice
        self.base = newPrice

    @api.depends("iva", "base")
    def computeTotalIVA(self):
        for record in self:
            if record.iva == '10':
                record.totalIva = record.base + (record.base * 0.10)
            elif record.iva == '21':
                record.totalIva = record.base + (record.base * 0.21)
            elif record.iva == '0':
                record.totalIva = record.base

    def confirmInvoice(self):
        self.state = 'Confirmed'

    def desactivateInvoices(self):
        invoices = self.search([('state','=','Confirmed')])
        for invoice in invoices:
            invoice.active = False
