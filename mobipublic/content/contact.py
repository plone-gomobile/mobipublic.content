from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.namedfile.field import NamedImage

# Interface class; used to define content-type schema.

class IContact(form.Schema):
    """
    Directory entry
    """
    
    phoneNumber = schema.TextLine(title=u"Tel Number (landline)", description=u"Must be in international format and start with +", required=False)

    mobileNumber = schema.TextLine(title=u"Mobile Number", description=u"Must be in international format and start with +", required=False)

class Contact(dexterity.Item):
    grok.implements(IContact)
    
    # Add your class methods and properties here

# View class
# The view will automatically use a similarly named template in
# Contact_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IContact)
    grok.require('zope2.View')
    grok.name("view")
    
    def formattedNumber(self, number):
        if number == None or number == "":
            return None
        
        helper = self.context.unrestrictedTraverse("phone_number_formatter")
        return helper.format(number)

    def getPhoneNumberLink(self):
        
        return self.formattedNumber(self.context.phoneNumber)

    
    def getMobileNumberLink(self):
        
        return self.formattedNumber(self.context.mobileNumber)
