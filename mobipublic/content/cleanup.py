import logging

import transaction
from zope import interface
from zope import component
import DateTime

from mobipublic.content import MessageFactory as _

import zExceptions

logger = logging.getLogger("mobipublic")

class CleanEvents(object):
    """ Clean-ups old events """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def clean(self, days, transaction_threshold=100):
        """ Perform clean-up by doing catalog search on events and turning
        old events private

        Commit ZODB transaction for every N objects to that commit buffer does not grow
        too long (timewise, memory wise).
        
        @param days: if item's ending day is older than this number of days it's removed

        @param transaction_threshold: How often we commit - for every nth item
        """
        logger.info("Beginning event clean up process")

        context = self.context.aq_inner
        count = 0

        
        day = DateTime.DateTime() - days
        end = DateTime.DateTime(day.year(), day.month(), day.day(), 23, 59, 59)
        
        date_range_query = { 'query':(end), 'range': 'max'} 
        path = '/'.join(context.getPhysicalPath())
        items = context.portal_catalog.queryCatalog({"portal_type":"Event",
                                                     "portal_state":"published",
                                                     "end": date_range_query,
                                                     "path": {"query": path, "depth": 10}})

        items = list(items)
        
        logger.info("Found %d events to be purged" % len(items))
        
        for b in items:
            count += 1            
            obj = b.getObject()
            logger.info("Deleting:" + obj.absolute_url() + " " + str(obj.endDate))
            obj.aq_parent.manage_delObjects([obj.getId()])

            if count % transaction_threshold == 0:
                # Prevent transaction becoming too large (memory buffer)
                # by committing now and then
                logger.info("Committing transaction")
                transaction.commit()

        msg = "Total %d items removed" % count
        logger.info(msg)

        return msg

    def __call__(self):

        days = self.request.form.get("days", None)
        if not days:
            raise zExceptions.InternalError("Bad input. Please give days=1 as HTTP GET query parameter")

        days = int(days)
        
        transaction_threshold = self.request.form.get("transaction_threshold", None)
        
        if transaction_threshold != None:        
            transaction_threshold = int(transaction_threshold)
   
            return self.clean(days, transaction_threshold)
        
        return self.clean(days)