from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Media
from .serializers import MediaSerializer
from .ai_utils import process_media


class MediaCreateView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def perform_create(self, serializer):
        media = serializer.save()
        driving_video_path = media.driving_video.path
        input_image_path = media.input_image.path
        output_video_path = f'media/output_animations/output_{media.id}.mp4'

        process_media(driving_video_path, input_image_path, output_video_path)

        media.output_video = output_video_path
        media.save()

    def create(self, request, *args, **kwargs):
        # Call the parent class's create method to handle the POST request and save the instance
        response = super().create(request, *args, **kwargs)

        # Retrieve the newly created Media instance
        media = self.get_queryset().get(id=response.data['id'])

        # Construct the URL for the output video
        output_video_url = request.build_absolute_uri(media.output_video.url)

        # Update the response data to include the URL of the output video
        response.data['output_video'] = output_video_url

        return response


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class MediaDetailView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer





