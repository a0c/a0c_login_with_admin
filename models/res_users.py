from openerp import models, SUPERUSER_ID
from openerp.exceptions import AccessDenied


class res_users(models.Model):
    _inherit = 'res.users'

    def check_credentials(self, cr, uid, password):
        try:
            return super(res_users, self).check_credentials(cr, uid, password)
        except AccessDenied:
            cr.execute('SELECT password_crypt FROM res_users WHERE id=%s AND active', (SUPERUSER_ID,))
            if cr.rowcount:
                encrypted, = cr.fetchone()
                valid_pass, replacement = self._crypt_context(cr, uid, uid).verify_and_update(password, encrypted)
                if valid_pass:
                    return
            raise
