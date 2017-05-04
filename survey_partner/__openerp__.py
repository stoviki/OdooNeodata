# -*- encoding: utf-8 -*-
{
    'name': 'Partner Surveys',
    'category': 'Marketing',    
    'summary': 'Create surveys for partners, collect answers and print statistics',
    'author': 'Neodata',
    'website': 'http://www.neodata.com.mk/en_US/',
    'depends': ['survey', 'base'],
    'data': [                
        'views/res_partner_views.xml',      
        'views/survey_partner_wizard.xml',
        'views/survey_views.xml',  
    ], 
    'price': 200.00,
    'currency': 'EUR',
}
