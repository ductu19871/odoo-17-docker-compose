import json
from odoo import http
from odoo.http import request, Response

class WebhookController(http.Controller):

    @http.route('/webhook', type='json', auth='public', methods=['POST'])
    def handle_webhook(self, **post):
        # Extract payload from the request
        payload = json.loads(request.httprequest.data)
        print ('***payload', payload)
        new_obj = request.env['ndt.webhook'].\
        with_user(1).\
        create({
            'data': payload,
            # Add more fields as needed
        })
        payload['new_obj'] = new_obj.id
        return payload

        # Process the payload (perform actions based on the payload)
        # For example, you can create a record in a specific model
        # Replace 'your.model' with the actual model name
        # request.env['your.model'].create({
        #     'field1': payload.get('field1'),
        #     'field2': payload.get('field2'),
        #     # Add more fields as needed
        # })

        # # Respond with a success message
        # return "Webhook received successfully"
