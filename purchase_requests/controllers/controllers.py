# from odoo import http
# from odoo.http import request
# import json
#
#
# # class PurchaseRequests(http.Controller):
# #     @http.route('/purchase_requests/purchase_requests', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"
# #
# #     @http.route('/purchase_requests/purchase_requests/objects', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('purchase_requests.listing', {
# #             'root': '/purchase_requests/purchase_requests',
# #             'objects': http.request.env['purchase_requests.purchase_requests'].search([]),
# #         })
# #
# #     @http.route('/purchase_requests/purchase_requests/objects/<model("purchase_requests.purchase_requests"):obj>', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('purchase_requests.object', {
# #             'object': obj
# #         })
#
# class ProductController(http.Controller):
#     # This controller provides an API endpoint to retrieve product information
#     # It returns a list of products with their details in JSON format
#     @http.route('/api/products', auth='public' , methods=['GET'], type='json' , csrf=False)
#     def get_products(self):
#         products = request.env['product.product'].sudo().search([] , limit=100)
#         result = []
#         for product in products:
#             result.append({
#                 'id': product.id,
#                 'name': product.name,
#                 'default_code': product.default_code,
#                 'standard_price': product.standard_price,
#                 'list_price': product.list_price,
#                 'qty_available': product.qty_available,
#             })
#         return {
#             'status': '200',
#             'data': result,
#         }
#     # This controller provides an API endpoint to retrieve customer information
#     # It returns a list of customers with their details in JSON format
#     @http.route('/api/customers', auth='public', methods=['GET'], type='json', csrf=False)
#     def get_products(self):
#         customers = request.env['res.partner'].sudo().search(['customer_rank','>',0], limit=100)
#         result = []
#         for customer in customers:
#             result.append({
#               'id':customer.id
#                 ,'name':customer.name,
#                 'email': customer.email,
#                 'phone': customer.phone,
#                 'street': customer.street,
#                 'city': customer.city,
#                 'zip': customer.zip,
#             })
#         return {
#             'status': '200',
#             'data': result,
#         }
#
