from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Media
from .serializers import MediaSerializer
from .ai_utils import process_media
from ai.inference import run_inference
from core.settings import DOMAIN


class MediaCreateView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        media = self.get_queryset().get(id=response.data['id'])
        driving_video_path = media.driving_video.path
        input_image_path = media.input_image.path
        output_path = f'media/output_animations/output_{media.id}'

        wfp, wfp_concat = run_inference(input_image_path, driving_video_path, output_path)
        wfp_url = f"{DOMAIN}/{wfp}"
        wfp_concat_url = f"{DOMAIN}/{wfp_concat}"

        admin_path = wfp.replace('media/', '', 1)  # The admin path needs to be modified, removing the 'media/'

        media.output_video = admin_path
        media.save()
        response.data['output_video'] = wfp_url
        return response


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class MediaDetailView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
