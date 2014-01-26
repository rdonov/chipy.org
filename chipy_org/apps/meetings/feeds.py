from django_ical.views import ICalFeed
from .models import Meeting
from datetime import timedelta

class MeetingFeed(ICalFeed):
    """
    A iCal feed for meetings
    """
    product_id = '-//chipy.org//Meeting//EN'
    timezone = 'CST'

    def items(self):
        return Meeting.objects.order_by('-when').all()

    def item_description(self, item):
        description = 'RSVP at http://chipy.org\n\n'
        for topic in item.topics.all():
            description += '{title} by {speaker}\n{description}\n\n'.format(
                title=topic.title, 
                speaker=topic.presentors.all()[0].name,
                description=topic.description)
        return description 

    def item_link(self, item):
        return ''

    def item_location(self, item):
        return item.where.address

    def item_start_datetime(self, item):
        return item.when
    
    def item_end_datetime(self, item):
        return item.when + timedelta(hours=1)

    def item_title(self, item):
        return 'ChiPy Meeting'