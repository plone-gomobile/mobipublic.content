from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IDeal(form.Schema):
    """
    Deals and discounts item
    """
    
    validUntil = schema.Datetime(title=u"Valid until")
    
    company = schema.TextLine(title=u"Company", required=False)
    
    website = schema.TextLine(title=u"Website", required=False)
    
    email = schema.TextLine(title=u"Email", required=False)
    
    phoneNumber = schema.TextLine(title=u"Phone", required=False)
    
    address = schema.TextLine(title=u"Address", required=False)
    
    postalCode = schema.TextLine(title=u"Postal code", required=False)
    
    city = schema.TextLine(title=u"City", required=False)
     
    contactPerson = schema.TextLine(title=u"Contact person", required=False)
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Deal(dexterity.Item):
    grok.implements(IDeal)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# deal_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IDeal)
    grok.name("view")
    grok.require('zope2.View')
    
    # grok.name('view')
    
    def getPhoneNumberLink(self):
        
        if self.context.phoneNumber == None or self.context.phoneNumber == "":
            return None
        
        helper = self.context.unrestrictedTraverse("phone_number_formatter")
        return helper.format(self.context.phoneNumber)
    