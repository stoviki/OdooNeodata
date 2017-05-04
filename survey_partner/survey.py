# -*- encoding: utf-8 -*-
from openerp.osv import osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class survey_survey(osv.Model):    
    _inherit = 'survey.survey'

    def evaluate_customer(self, cr, uid, ids, context=None):    
        print context   
        context = dict(context or {}, relative_url=True)     
        context['default_survey_id'] = ids[0]   
        return {
                'type': 'ir.actions.act_window',
                'name': _('Ask Customer'),
                'src_model': 'survey.survey',
                'res_model': 'survey.partner.wizard',                
                'view_mode': 'form',
                'target': 'new',
                'key2': 'client_action_multi',
                'context': context
        }
        
class survey_user_input(osv.Model):    
    _inherit = 'survey.user_input'

    def action_view_answers(self, cr, uid, ids, context=None):
        ''' Open the website page with the survey form '''
        context = dict(context or {}, relative_url=True)
        user_input = self.read(cr, uid, ids, ['print_url', 'token'], context=context)[0]
        return {
            'type': 'ir.actions.act_url',
            'name': "View Answers",
            'target': 'self',
            'url': '%s/%s' % (user_input['print_url'], user_input['token'])
        }
        
    def action_survey_results(self, cr, uid, ids, context=None):
        ''' Open the website page with the survey results '''
        context = dict(context or {}, relative_url=True)
        return {
            'type': 'ir.actions.act_url',
            'name': "Survey Results",
            'target': 'self',
            'url': self.read(cr, uid, ids, ['result_url'], context=context)[0]['result_url']
        }