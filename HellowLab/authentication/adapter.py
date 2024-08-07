# adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        context['sitedomain'] = settings.URL_FRONT
        context['sitename'] = settings.SITE_NAME
        # if 'key' in context:
        #     context['activate_url'] = settings.URL_FRONT + 'login/email/confirm/' + context['key']
        if 'password_reset_url' in context:
            context['password_reset_url'] = context['password_reset_url'].replace("http://tagsdnekcab.mgbcengineering.com/api/auth/password/reset/confirm/", settings.URL_FRONT + 'login/forgotpassword/confirm/')
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
