from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
 

@python_2_unicode_compatible
class Activity(models.Model):
    LIKE = 'L'
    LIKE_PROFILE = 'LP' 
    ACTIVITY_TYPES = (
        (LIKE, 'Like'), 
        (LIKE_PROFILE,'Like Profile'), 
        ) 

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=5, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    profile = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type


@python_2_unicode_compatible
class Notification(models.Model):
    LIKED = 'L'
    LIKED_PROFILE = 'LP'
    COMMENTED = 'C'
    ALSO_COMMENTED = 'S'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (LIKED_PROFILE,'Liked Profile'),
        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also Commented'),
        )
    #profile liked template
    _LIKED_TEMPLATE_PROFILE = '<a href="/{0}/">{1}</a> liked you, Now {1} can write on your profile, stop <a href="/{0}/">{1}</a>'  # noqa: E501
    _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    profile = models.ForeignKey('authentication.profile', null=True, blank=True)
    notification_type = models.CharField(max_length=5,
                                         choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification' 
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        #added for notifications on profiles like 
        if self.notification_type == self.LIKED_PROFILE:
            return self._LIKED_TEMPLATE_PROFILE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                # escape(self.to_user.username),
                # self.profile.pk,
                # escape(self.get_summary(self.profile.user.username))
                )
            #end profile likes notifications
        elif self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value
