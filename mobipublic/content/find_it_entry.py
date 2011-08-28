from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from mobipublic.content import MessageFactory as _

from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from Products.CMFCore.utils import getToolByName

from mobile.heurestics import poi, simple
from mobile.heurestics.vcard import is_vcard_supported 

from gomobile.mobile.utilities import get_host
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
    city = schema.TextLine(title=u"City", required=False)
    
    latitude = schema.Float(title=u"Latitude", required=False, description=u"Required for mini map")
    longitude = schema.Float(title=u"Longitude", required=False, description=u"Required for mini map")
    
    website = schema.TextLine(title=u"Website", required=False, description=u"Must start with http://")
    email = schema.TextLine(title=u"Email", required=False)
    phoneNumber = schema.TextLine(title=u"Phone number (primary)", description=u"Must be in international format and start with +", required=False)
    phoneNumber2 = schema.TextLine(title=u"Phone number (secondary)", description=u"Must be in international format and start with +",required=False)
    
    tags = schema.TextLine(title=u"Phone number (secondary)", required=False)
    
    openingTimes = schema.Text(title=u"Opening hours", description=u"One day per line - free format", required=False)

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
    
    def get_property(self, property_name, default=None):
        """ Get property of a given name from the the site setting """
        
        portal_properties = getToolByName(self, 'portal_properties')
        properties = portal_properties.mobipublic_properties        
        return getattr(properties, property_name, default)
            
    
    def get_google_map_api_key_for_current_domain(self):
        """
        Some magic to fetch domain specific Maps API key.
        
        You need API key as google_map_api_key_en or google_map_api_key_mobipublic_com
        """
        
        host = get_host(self.request)
        
        domain = host.split(":")[0]        
        domain = domain.replace(".","_")
                                        
        property_name = "google_map_api_key_" + domain
        print "Map key property:" + property_name
        
        key = self.get_property(property_name)
        print "Got key:" + str(key)

        return key

    def latitude(self):
        return self.context.latitude
    
    def longitude(self):
        return self.context.longitude
    
    def has_location(self):
        """
        """
        return self.context.longitude != None and self.context.latitude != None 

    def is_landmark(self):
        if not self.has_location():
            return False
        return poi.get_poi_type(self.request) == "landmark"

    def is_map_link(self):
        if not self.has_location():
            return False
        return poi.get_poi_type(self.request) == "href"

    def get_map_link(self):
        
        try:
            lat = float(self.context.latitude)
            long = float(self.context.longitude)
        except:
            # Avoid possible float formatting problems
            lat = 0
            long = 0
            
        return poi.get_google_maps_link(lat, long)
    
    def getPhoneNumberLink(self):
        
        if self.context.phoneNumber == None or self.context.phoneNumber == "":
            return None
        
        helper = self.context.unrestrictedTraverse("phone_number_formatter")
        return helper.format(self.context.phoneNumber)
    
    
    def is_vcard_supported(self):
        supported = is_vcard_supported(self.request)
        return supported
    