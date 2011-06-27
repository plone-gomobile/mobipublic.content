"""

"""




def test(context):
    from StrinIO import StringIO
    from DateTime import DateTime
    
    buf = ""
    
    # Purge items from ten years past to half year past
    end = DateTime() - 180*24*3600.0 # Half year past
    start = DateTime() - 10*365*24*3600.0 # Ten years part
    
    items = context.portal_catalog(portal_type="FeedFeederItem", created = {'date': {'query':(start, end), 'range': 'min:max'}})
    count = len(list(items))
    buf += "Found %d old items\n" % count 
    
    for brain in items:
            #obj = brain.getObject()
            buf += "Deleting item " + brain.getURL() + " " + str(brain.created) + "\n"
            #obj.aq_parent.manage_delObjects([obj])
    
    return buf

