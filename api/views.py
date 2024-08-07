import requests
from rest_framework import generics
from .models import Media
from .serializers import MediaSerializer

# URL for FastAPI service
FASTAPI_URL = 'http://localhost:8080/generate_video'


class MediaCreateView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        media = self.get_queryset().get(id=response.data['id'])
        driving_video = media.driving_video
        input_image = media.input_image
        output_path = f'media/output_animations/output_{media.id}'

      # Prepare files for FastAPI request
        files = {
            'source': (input_image.name, input_image.file),
            'driving': (driving_video.name, driving_video.file),
        }
        
        data = {
            'output_dir': output_path
        }

        try:
            # Send a request to FastAPI
            fastapi_response = requests.post(
                'http://localhost:8080/generate_video',
                files=files,
                data=data
            )
            # Check if the request was successful
            fastapi_response.raise_for_status()

            # Get the response data from FastAPI
            response_data = fastapi_response.json()
            wfp_url = response_data.get('output_video_path')
            wfp_concat_url = response_data.get('concatenated_video_path')

            # Update media object with FastAPI response
            admin_path = output_path.replace('media/', '', 1)  # Adjust path if needed
            media.output_video = admin_path
            media.save()

            response.data['output_video'] = wfp_url
            response.data['concatenated_video'] = wfp_concat_url

        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            response.data['error'] = str(e)
            response.status_code = 500

        return response


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class MediaDetailView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
