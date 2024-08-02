# -*- coding: utf-8 -*-
# from odoo import http


# class Pdam(http.Controller):
#     @http.route('/pdam/pdam/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pdam/pdam/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pdam.listing', {
#             'root': '/pdam/pdam',
#             'objects': http.request.env['pdam.pdam'].search([]),
#         })

#     @http.route('/pdam/pdam/objects/<model("pdam.pdam"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pdam.object', {
#             'object': obj
#         })
