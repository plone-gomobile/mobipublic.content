from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from plone.namedfile.field import NamedImage

# Interface class; used to define content-type schema.

class IBlogEntry(form.Schema):
    """
    Image and text
    """
 
    form.widget(bodyText=WysiwygFieldWidget)
    bodyText = schema.Text(title=u"Body text", 
                           description=u"Longer, HTML formatted description, which is displayed when the page is opened",
                           required=False)
     
    image = NamedImage(title=u"Image", 
                               description=u"Will be automatically resized", 
                               required=False)

    


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class BlogEntry(dexterity.Item):
    grok.implements(IBlogEntry)
    
    # Add your class methods and properties here



class View(grok.View):
    grok.context(IBlogEntry)
    grok.require('zope2.View')
    grok.name("view")