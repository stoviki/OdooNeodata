from openerp import models, api
from openerp.osv import fields
from openerp.tools.translate import _

class survey_partner_wizard(models.TransientModel):
    _name = 'survey.partner.wizard'
    _description = 'Survey Partner Wizard'

    _columns = {
        'partner_id': fields.many2one('res.partner', string='Customer'),
        'survey_id': fields.many2one('survey.survey', string='Survey'),
    }
    
    @api.multi
    def evaluate_customer(self):      
        url = self.survey_id.read(['public_url'])[0]['public_url'] + "/phantom"
        if self.partner_id:
            url = self.survey_id.read(['public_url'])[0]['public_url'] + '/' + str(self.partner_id.id) + "/phantom"
        return {
            'type': 'ir.actions.act_url',
            'name': "Results of the Survey",
            'target': 'self',
            'url': url,
        }