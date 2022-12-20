import io
import json

import xlsxwriter

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class CustomMrpProduction(models.Model):
    _inherit = 'mrp.production'

    mv_workorder_number = fields.Char(string='MV Work Order Number')

    def import_bom(self):
        bom = self.env['mrp.bom']._bom_find(self.product_id, company_id=self.company_id.id, )[self.product_id]
        print(bom)
        if bom:
            self.bom_id = bom.id
            print(self.bom_id.product_tmpl_id.name)
            query = """ select mbl.bom_id, pt.name, mbl.product_qty
                        from mrp_bom as  mb
                        inner join mrp_bom_line as mbl
                        on mbl.bom_id = mb.id
                        inner join product_product as pd
                        on pd.id = mbl.product_id
                        inner join product_template as pt
                        on pd.product_tmpl_id = pt.id where mb.id = '%d' """ % bom.id
            self.env.cr.execute(query)
            query_data = self.env.cr.dictfetchall()
            print(query_data)
            data = {
                'bom': query_data
            }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'mrp.production',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'BoM Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise ValidationError('No bill of material is available for the selected product')

    def get_xlsx_report(self, data, response):
        # bufferoutput'for writing data into Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        product_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '15px'})
        col_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '13px'})
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)

        if data.get('bom'):
            bom = data.get('bom')
            if bom:
                row = 0
                col = 0
                sheet.write(row, col, 'Components', product_name)
                sheet.write(row, col + 1, 'To Consume', col_name)
                rows = 0
                cols = 0
                for rec in bom:
                    rows = rows + 1
                    sheet.write(rows, cols, rec.get('name'))
                    sheet.write(rows, cols + 1, rec.get('product_qty'))
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
