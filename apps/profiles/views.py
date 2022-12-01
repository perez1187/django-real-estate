from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer


"""
    from rest_framework import api_view, permissions
    @api_view(["GET"])
    @permission_classes((permissions.IsAuthenticated))
    def get_all_agents(request):
        agents = Profile.objects.filter(is_agent=True)
        serializer=ProfileSerializer(agents, many=True)
        name_spaced_response={"agents": serializer.data}
        return Response(name_spaced_response,status=status.HTTP_200_OK)
"""


class TopAgentsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer


class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]  # so we will see profile: data

    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(
            user_profile, context={"request": request}
        )  # 2:33
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )  # and we use renderer classes here


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        # here we check if profile exist
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound  # we raise custo exception

        # here we check if user from token  is the same user that we want to change
        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile  # another custom exception

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        serializer.is_valid()  # if evertyhing is good we can save it
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
