from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.namedfile.field import NamedImage
# Interface class; used to define content-type schema.

# Interface class; used to define content-type schema.

class IMovie(form.Schema):
    """
    Movie
    """
    
        
    #website = schema.TextLine(title=u"Website", required=False)
    
    #email = schema.TextLine(title=u"Email", required=False)
    
    #phoneNumber = schema.TextLine(title=u"Primary number", required=False)
    
    #otherPhoneNumbers = schema.TextLine(title=u"Other phone numbers", required=False)

    location = schema.TextLine(title=u"Location", required=False)

    screen = schema.Choice(
            title=u"Screen",
            values=(1,2,3,4,5,6),
            required=True
        )
    
    #address = schema.TextLine(title=u"Address", required=False)
    
    #postalCode = schema.TextLine(title=u"Postal code", required=False)
    
    #city = schema.TextLine(title=u"City", required=False)
     
    #contactPerson = schema.TextLine(title=u"Contact person", required=False)
    
    #image = NamedImage(title=u"Image", 
    #                           description=u"Will be automatically resized", 
    #                           required=False)
    
    openingTimes = schema.Text(title=u"Opening hours", description=u"One day per line - free format", required=False)
    

    form.widget(bodyText=WysiwygFieldWidget)
    bodyText = schema.Text(title=u"Body text", 
                           description=u"Longer, HTML formatted description, which is displayed when the page is opened",
                           required=False)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Movie(dexterity.Item):
    grok.implements(IMovie)
    
    # Add your class methods and properties here


class View(grok.View):
    grok.context(IMovie)
    grok.name("view")
    grok.require('zope2.View')
    
    # grok.name('view')