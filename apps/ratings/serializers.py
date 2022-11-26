from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        exclude = ["updated_at", "pkid"]

    ''' 
        when we have SerializerMethodField we need to hahave get_<name>
        and return we are looking for a path to username
    '''
    def get_rater(self, obj):
        return obj.rater.username # model i s Rating, rater is user

    def get_agent(self, obj):
        return obj.agent.user.username  # aget -> Profile Foreign Key, user and after user we have username