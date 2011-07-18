from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.namedfile.field import NamedImage

# Interface class; used to define content-type schema.

class ILink(form.Schema):
    """
    Directory entry
    """
    
    remoteUrl = schema.URI(title=u"URL", required=True)

    screenshot = NamedImage(title=u"Screenshot", 
                               description=u"Will be automatically resized", 
                               required=False)


class Link(dexterity.Item):
    grok.implements(ILink)
    
    # Add your class methods and properties here

    def getRemoteUrl(self):
        """ Indexing compatibility moethod """
        return self.remoteUrl

# View class
# The view will automatically use a similarly named template in
# link_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(ILink)
    grok.require('zope2.View')
    grok.name("view")
    
    def hasImage(self):
        """
        """
        return self.context.screenshot != None
    
    def getImageURL(self):
        """
        """
        return 
    # grok.name('view')