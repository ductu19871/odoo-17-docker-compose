from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import os
from  datetime import datetime

def speedtest(func):
    def wrapper(*arg,**kw):
        current_time = datetime.now()
        rs  = func(*arg, **kw)
        current_time2 = datetime.now()
        time_difference = current_time2 - current_time
        seconds_difference = time_difference.total_seconds() 
        print ('**seconds_difference %s'%func.__name__, seconds_difference)
        return rs
    return wrapper


class AM(models.Model):
    _inherit = 'account.move'

    ndt_payment_ids = fields.One2many('account.payment', 'move_id')
    count_ndt_payment = fields.Integer(compute='_compute_count_ndt_payment')
    is_trigger = fields.Boolean()
    payment_state_old = fields.Char()

    @api.depends('is_trigger')
    def _compute_payment_state(self):
        return super()._compute_payment_state()
    
    @speedtest
    def do_st(self, batch_moves, file_path2):
        for move in batch_moves:
            try:
                for l in move.line_ids:
                    pass
                    # print ('** l.matched_debit_ids**', [(6,0,l.matched_debit_ids.ids)])
                    # l.write({'matched_debit_ids': [(6,0, list(l.matched_debit_ids.ids))]})
                move.write({'state': move.state})
            except Exception as e:
                print (e)
                with open(file_path2, 'a', encoding='utf-8') as file:
                    # Convert the integer to a string and write it to xthe file
                    file.write(str(e) + r'\n')
    @speedtest
    def recompute_payment_state(self, limit=0, offset=0, add_domain=[], n_split=100, domain=None):

        file_dir = r'C:\Users\TU\Desktop\1'  # Replace with your desired directory
        file_path = os.path.join(file_dir, 'output.txt')
        file_path2 = os.path.join(file_dir, 'output_error.txt')
        # Ensure the directory exists
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


        if  offset ==None:
            try:
            # Open the file in read mode
                with open(file_path, 'r') as file:
                    # Read the content of the file
                    content = file.read()
                    # Convert the content to an integer
                    offset = int(content)
            except: 
                offset = offset
        if not domain:
            dm = [('move_type', 'in', ('out_invoice', 'in_invoice'))]
        else:
            dm = domain
        dm += add_domain
        account_moves = self.env['account.move'].search(dm, limit=limit, offset=offset)
        
        # n_split = 300  # Number of records to process in each batch
        total_moves = len(account_moves)
        for i in range(0, total_moves, n_split):
            batch_moves = account_moves[i:i + n_split]  # Get a batch of records
            
            # Update the state for each record in the batch
            # for move in batch_moves:
            self.do_st(batch_moves, file_path2)
                # try:
                #     for l in move.line_ids:
                #         l.write({'matched_debit_ids': l.matched_debit_ids})
                #     move.write({'state': move.state})
                # except Exception as e:
                #     print (e)
                #     with open(file_path2, 'a', encoding='utf-8') as file:
                #         # Convert the integer to a string and write it to the file
                #         file.write(str(e))


            
            # Commit the changes
            # self.env.cr.rollback()
            self.env.cr.commit()
            print ('i đã commit', i)

            with open(file_path, 'w') as file:
                # Convert the integer to a string and write it to the file
                file.write(str(offset + i + n_split))
    
    def _compute_count_ndt_payment(self):
        for r in self:
            r.count_ndt_payment = len(r.ndt_payment_ids)
        
   

    # @api.model
    # def _search_default_journal(self, journal_types):
    #     company_id = self._context.get('default_company_id', self.env.company.id)
    #     warehouse_id = self._context.get('overwrite_user_warehouse_id') or self.env.user.warehouse_id

    #     domain = [('company_id', '=', company_id), ('type', 'in', journal_types), ('warehouse_id','=', warehouse_id.id)]# custome only here
    #     journal = self.env['account.journal'].search(domain, limit=1)
    #     if journal:
    #         return journal
    #     else:
    #         return super(AM, self)._search_default_journal(journal_types)
        # journal = None
        # if self._context.get('default_currency_id'):
        #     currency_domain = domain + [('currency_id', '=', self._context['default_currency_id'])]
        #     journal = self.env['account.journal'].search(currency_domain, limit=1)

        # if not journal:
        #     journal = self.env['account.journal'].search(domain, limit=1)

        # if not journal:
        #     company = self.env['res.company'].browse(company_id)

        #     error_msg = _(
        #         "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
        #         company_name=company.display_name,
        #         journal_types=', '.join(journal_types),
        #     )
        #     raise UserError(error_msg)

        # return journal

    # @api.model
    # def _get_default_journal(self):
    #     ''' Get the default journal.
    #     It could either be passed through the context using the 'default_journal_id' key containing its id,
    #     either be determined by the default type.
    #     '''
    #     move_type = self._context.get('default_move_type', 'entry')
    #     if move_type in self.get_sale_types(include_receipts=True):
    #         journal_types = ['sale']
    #     elif move_type in self.get_purchase_types(include_receipts=True):
    #         journal_types = ['purchase']
    #     else:
    #         journal_types = self._context.get('default_move_journal_types', ['general'])

    #     if self._context.get('default_journal_id'):
    #         journal = self.env['account.journal'].browse(self._context['default_journal_id'])

    #         if move_type != 'entry' and journal.type not in journal_types:
    #             raise UserError(_(
    #                 "Cannot create an invoice of type %(move_type)s with a journal having %(journal_type)s as type.",
    #                 move_type=move_type,
    #                 journal_type=journal.type,
    #             ))
    #     else:
    #         journal = self._search_default_journal(journal_types)

    #     return journal
