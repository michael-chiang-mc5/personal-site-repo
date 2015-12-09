from django.db import models
import json
from django.contrib.auth.models import User
import datetime
from bson import json_util
from django.utils.timesince import timesince

class MCPost(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True)
    mother = models.ForeignKey('self', blank=True, null=True)
    text_history = models.TextField() # This is a json serialized string that contains history of text content of post
    node_depth = models.PositiveIntegerField() # base node posts have a node depth of 0
    deleted = models.BooleanField(default=False)
    upvoters   = models.ManyToManyField(User, blank=True, related_name="upvoted")
    downvoters = models.ManyToManyField(User, blank=True, related_name="downvoted")

    # Returns post text of the most recent edit
    def __str__(self):
        return self.text_history
    # This method allows a given user to edit post text. Previous text is saved
    # text: edited post text
    # user_pk: user that is editing the post
    def edit(self,text,user_pk):
        date = datetime.datetime.now()
        edit = (text,user_pk,date)
        if self.text_history: # if there is previous post content, append
            history = self.deserialize()
            history.append(edit)
        else:
            history = []
            history.append(edit)
        self.text_history = self.serialize(history)

    def serialize(self, obj):
        return json.dumps(obj, default=json_util.default)

    # This method deserializes MCPost.text_history into vector of tuples
    # rn[i] = (text , user_pk , date)
    def deserialize(self):
        return json.loads(self.text_history, object_hook=json_util.object_hook)
    def get_most_recent_text(self):
        edit = self.get_most_recent_edit_tuple()
        return edit[0]
    def get_most_recent_user(self):
        edit = self.get_most_recent_edit_tuple()
        return edit[1]
    def get_most_recent_date(self):
        edit = self.get_most_recent_edit_tuple()
        return edit[2]
    def get_most_recent_edit_tuple(self):
        edits = self.deserialize()
        edit = edits[-1]
        return edit

    def get_original_age(self):
        return self.get_age(self.time)
        
    @staticmethod
    def get_age(time):
        now = datetime.datetime.now(datetime.timezone.utc)
        try:
            difference = now - time
        except:
            return "Invalid input"
        if difference <= datetime.timedelta(minutes=1):
            return 'just now'
        return '%(time)s ago' % {'time': timesince(time).split(', ')[0]}

    def get_edit_history(self):
        tuple_list = self.deserialize()
        rn = []
        for count,t in enumerate(tuple_list):
            entry = ''
            # did the original post author make the edit?
            original_user_pk = self.user.pk
            editing_user_pk = int(t[1])
            if original_user_pk!=editing_user_pk:
                editing_user = User.objects.get(pk=editing_user_pk)
                entry += editing_user.username + ' '
            # is this an original post or edit?
            if count==0:
                entry+='posted '
            else:
                entry += 'edited '
            # get time edited
            entry += self.get_age(t[2])
            rn.append(entry)
        # return
        return rn



    def score(self):
        if self.deleted:
            return -999999
        else:
            return len(self.upvoters.all()) - len(self.downvoters.all())

    # This method returns an unordered list of all children, including self
    def get_subtree(self):
        rn = []
        rn.append(self)
        for post in MCPost.objects.filter(mother=self):
            subtree = post.get_subtree()
            rn = rn + subtree
        return rn
