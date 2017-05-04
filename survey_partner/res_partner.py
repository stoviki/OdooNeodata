from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_partner(osv.Model):
    _inherit = "res.partner"
    _columns = {
        'survey_input_ids': fields.one2many('survey.user_input', 'partner_id', 'Survey Input'),
        'survey_ids': fields.many2many('survey.survey', 'partner_suurvey_rel', 'partner_id', 'survey_id', 'Surveys')
    }