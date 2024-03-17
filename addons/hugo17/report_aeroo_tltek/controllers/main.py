# -*- encoding: utf-8 -*-
import werkzeug
import json
import time
from odoo import api, http, _
from odoo.modules import registry
from odoo.http import route, request, content_disposition
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, time
from odoo.addons.web.controllers import main
from odoo.addons.http_routing.models.ir_http import slugify

MIMETYPES_MAPPING = {
    'doc': 'application/vnd.ms-word',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odt': 'application/vnd.oasis.opendocument.text',
    'pdf': 'application/pdf',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'zip': 'application/zip',
}

DEFAULT_MIMETYPE = 'octet-stream'

# class ReportController(main.ReportController):
#
#     @route()
#     def report_routes(self, reportname, docids=None, converter=None, **data):
#         report = request.env['ir.actions.report']._get_report_from_name(reportname)
#         context = dict(request.env.context)
#
#         if docids:
#             docids = [int(i) for i in docids.split(',')]
#         if data.get('options'):
#             data.update(json.loads(data.pop('options')))
#         if data.get('context'):
#             data['context'] = json.loads(data['context'])
#             context.update(data['context'])
#         if converter == 'html':
#             html = report.with_context(context)._render_qweb_html(docids, data=data)[0]
#             return request.make_response(html)
#         elif converter == 'pdf':
#             pdf = report.with_context(context)._render_qweb_pdf(docids, data=data)[0]
#             pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
#             if report.open_browser:
#                 filename = "%s.pdf" % (report.name)
#                 if docids and len(docids) > 1 and report.print_report_name:
#                     obj = request.env[report.model].browse(docids)
#                     report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
#                     filename = "%s.pdf" % (report_name)
#                 pdfhttpheaders.append(("Content-Disposition", content_disposition(filename)))
#             return request.make_response(pdf, headers=pdfhttpheaders)
#         elif converter == 'text':
#             text = report.with_context(context)._render_qweb_text(docids, data=data)[0]
#             texthttpheaders = [('Content-Type', 'text/plain'), ('Content-Length', len(text))]
#             return request.make_response(text, headers=texthttpheaders)
#         else:
#             raise werkzeug.exceptions.HTTPException(description='Converter %s not implemented.' % converter)
#
#     @route()
#     def report_routes(self, reportname, docids=None, converter=None, **data):
#         report = request.env['ir.actions.report']._get_report_from_name(reportname)
#         if converter == 'pdf' and report.open_browser:
#             context = dict(request.env.context)
#
#             if docids:
#                 docids = [int(i) for i in docids.split(',')]
#
#             if data.get('options'):
#                 data.update(json.loads(data.pop('options')))
#
#             if data.get('context'):
#                 data['context'] = json.loads(data['context'])
#                 context.update(data['context'])
#
#             pdf = report.with_context(context)._render_qweb_pdf(docids, data=data)[0]
#             filename = "%s" % (report.name)
#             if docids and report.print_report_name:
#                 obj = request.env[report.model].browse(docids)
#                 report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
#                 filename = "%s" % (report_name)
#
#             pdfhttpheaders = [
#                 ("Content-Type", "application/pdf"),
#                 ("Content-Length", len(pdf)),
#                 ('Content-Disposition', 'filename="%s.pdf"' % slugify(filename)),
#                             ]
#             return request.make_response(pdf, headers=pdfhttpheaders)
#
#         return super(ReportController, self).report_routes(reportname, docids=docids, converter=converter, **data)


class AerooReportController(http.Controller):

    @http.route('/web/report_aeroo', type='http', auth="user")
    def generate_aeroo_report(self, report_id, record_ids, token, debug=False):
        report_id = int(report_id)
        record_ids = json.loads(record_ids)

        report = request.env['ir.actions.report'].browse(report_id)
        aeroo, out_format = report._render_aeroo(record_ids)

        if len(record_ids) == 1:
            record = request.env[report.model].browse(record_ids[0])
            file_name = report.get_aeroo_filename(record, out_format)
        else:
            file_name = '%s.%s' % (report.name, out_format)

        report_mimetype = MIMETYPES_MAPPING.get(out_format, DEFAULT_MIMETYPE)

        response = request.make_response(
            aeroo,
            headers=[
                ('Content-Disposition', content_disposition(file_name)),
                ('Content-Type', report_mimetype),
                ('Content-Length', len(aeroo))],
            cookies={'fileToken': token})

        return response

    @staticmethod
    def _get_aeroo_report_from_name(report_name):
        """Get an aeroo report template from the given report name."""
        report = request.env['ir.actions.report'].search([
            ('report_name', '=', report_name),
        ])
        if not report:
            raise ValidationError(
                _('No aeroo report found with the name {report_name}.'),
                report_name=report_name)

        if len(report) > 1:
            report_display_names = '\n'.join(report.mapped('display_name'))
            raise ValidationError(_(
                'Multiple aeroo reports found with the same name ({report_name}):\n\n'
                '{report_display_names}').format(
                    report_name=report_name,
                    report_display_names=report_display_names))

        return report
