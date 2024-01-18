# -*- coding: utf-8 -*-
# from odoo import http


# class Trfflesapp(http.Controller):
#     @http.route('/trfflesapp/trfflesapp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trfflesapp/trfflesapp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trfflesapp.listing', {
#             'root': '/trfflesapp/trfflesapp',
#             'objects': http.request.env['trfflesapp.trfflesapp'].search([]),
#         })

#     @http.route('/trfflesapp/trfflesapp/objects/<model("trfflesapp.trfflesapp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trfflesapp.object', {
#             'object': obj
#         })
