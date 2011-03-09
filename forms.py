from flaskext.wtf import Form
from flaskext.wtf import TextField
from flaskext.wtf import TextAreaField
from flaskext.wtf import Required
from flaskext.wtf import BooleanField
from flaskext.wtf import HiddenField

from helpers import slugify

class TopicForm(Form):
    
    body = TextAreaField('Body', [Required()])
    category = TextField('Category', [Required()])
    name = TextField('Name', [Required()])
    published = BooleanField('Published')
    login_required = BooleanField('Login Required')
    system = HiddenField()
    
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(TopicForm, self).__init__(*args, **kwargs)

    def validate_category(form, field):
        return slugify(field.data)
        
class SystemForm(Form):

    name = TextField('Name', [Required()])
    description = TextAreaField('Description', [Required()])
    icon_url = TextField('Icon URL')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(SystemForm, self).__init__(*args, **kwargs)
    # def validate_icon_url(form, field):
    #     if field.data:
    #         print 'herefasdfasd'
    #         import urllib2
    #         try:
    #             req = urllib2.Request(field.data, None, None)
    #             urllib2.urlopen(req)
    #         except Exception, e:
    #             logging.info("exception %s" % e)
    #             raise ValidationError('Invalid URL')
            
