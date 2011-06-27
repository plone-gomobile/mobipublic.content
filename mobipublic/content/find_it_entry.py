from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget

# Interface class; used to define content-type schema.

class IFindItEntry(form.Schema):
    """
    Find it directory entry
    """

    form.widget(bodyText=WysiwygFieldWidget)
    bodyText = schema.Text(title=u"Body text", 
                           description=u"Longer, HTML formatted description, which is displayed when the page is opened",
                           required=False)

    address = schema.TextLine(title=u"Address", required=False)
    postalCode = schema.TextLine(title=u"Postal code", required=False)
    
    latitude = schema.TextLine(title=u"Latitude", required=False)
    longitude = schema.TextLine(title=u"Longitude", required=False)
    
    website = schema.TextLine(title=u"Website", required=False)
    email = schema.TextLine(title=u"Email", required=False)
    phoneNumber = schema.TextLine(title=u"Phone number (primary)", required=False)
    phoneNumber2 = schema.TextLine(title=u"Phone number (secondary)", required=False)
    
    tags = schema.TextLine(title=u"Phone number (secondary)", required=False)

    form.widget(tags=TextLinesFieldWidget)
    tags = schema.List(
            title=_(u"Tags"),
            description=_(u"One per line"),
            required=False,
            default=[],
            value_type=schema.TextLine(),
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class FindItEntry(dexterity.Item):
    grok.implements(IFindItEntry)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# find_it_entry_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class FindIt(grok.View):
    grok.context(IFindItEntry)
    grok.require('zope2.View')
    
    # grok.name('view')