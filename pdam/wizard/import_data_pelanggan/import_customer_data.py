from odoo import models, fields, api, _
from odoo.exceptions import UserError
from tempfile import TemporaryFile
from io import BytesIO
import base64
from datetime import datetime, timedelta, timezone
import openpyxl
import logging
from ...helpers.excel_reader_file import ExcelFileReader

_logger = logging.getLogger(__name__)


class ImportDataPelangganWizard(models.TransientModel):
    _name = "import.data.pelanggan.wizard"
    _description = "Wizard to create data student"

    filename = fields.Char("File Name", required=True)
    excel_file = fields.Binary('Excel File', required=True)

    def confirm(self):
        data = self.read_excel_file()
        self.create_customer_data(data)

    def read_excel_file(self):
        data = ExcelFileReader(self.excel_file).get_data()
        if not data:
            raise UserError(_("No Data Found in the file"))
        data = data[1:]
        return data

    def create_customer_data(self, data):
        self.env['part.student'].create([{
            'name': row[0],
            'student_card_number': row[1],
            'address_student': row[2],
            'gender': row[3],
            'religion': row[4],
            'bill_email_partner': row[5],
        } for row in data])
