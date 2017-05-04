# -*- coding: utf-8 -*-

import json
import logging
import werkzeug
import werkzeug.utils
from datetime import datetime
from math import ceil

from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from openerp.tools.safe_eval import safe_eval

from openerp.addons.survey.controllers import main


_logger = logging.getLogger(__name__)

class WebsiteSurveyPartner(main.WebsiteSurvey):
    ## ROUTES HANDLERS ##
    
    # Survey start
    @http.route(['/survey/start/<model("survey.survey"):survey>',
                 '/survey/start/<model("survey.survey"):survey>/<string:token>',
                 '/survey/start/<model("survey.survey"):survey>/<model("res.partner"):partner>/<string:token>'],
                type='http', auth='public', website=True)
    def start_survey(self, survey, partner=None, token=None, **post):
        print "DRNDRNDRN"
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        user_input_obj = request.registry['survey.user_input']

        # Test mode
        if token and token == "phantom":
            _logger.info("[survey] Phantom mode")
            if partner:
                user_input_vals = {'survey_id': survey.id, 'partner_id': partner.id, 'test_entry': True}
            else:
                user_input_vals = {'survey_id': survey.id, 'test_entry': True}
            user_input_id = user_input_obj.create(cr, uid, user_input_vals, context=context)
            user_input = user_input_obj.browse(cr, uid, [user_input_id], context=context)[0]
            data = {'survey': survey, 'page': None, 'token': user_input.token}
            return request.website.render('survey.survey_init', data)
        # END Test mode

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(cr, uid, request, survey_obj, survey, user_input_obj, context=context)
        if errpage:
            return errpage

        # Manual surveying
        if not token:
            vals = {'survey_id': survey.id}
            if request.website.user_id.id != uid:
                vals['partner_id'] = request.registry['res.users'].browse(cr, uid, uid, context=context).partner_id.id
            user_input_id = user_input_obj.create(cr, uid, vals, context=context)
            user_input = user_input_obj.browse(cr, uid, [user_input_id], context=context)[0]
        else:
            try:
                user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', token)], context=context)[0]
            except IndexError:  # Invalid token
                return request.website.render("website.403")
            else:
                user_input = user_input_obj.browse(cr, SUPERUSER_ID, [user_input_id], context=context)[0]

        # Do not open expired survey
        errpage = self._check_deadline(cr, uid, user_input, context=context)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # Intro page
            data = {'survey': survey, 'page': None, 'token': user_input.token}
            return request.website.render('survey.survey_init', data)
        else:
            return request.redirect('/survey/fill/%s/%s' % (survey.id, user_input.token))
