<p>
  <a href="https://exarth.com/">
  <img src="https://exarth.com/static/exarth/theme/logo-red-1000.svg" height="150">
  </a>
</p>
<hr>

# Animator AI

## Overview

The **Animator AI** is a Django-based application that allows users to upload media files (such as videos and images) and process them using AI models. The API takes an input image and a driving video, processes them to generate an animated output video, and returns a link to the generated video.

## Features

- **Media Upload:** Upload a driving video and an input image through the API.
- **AI Processing:** Process the uploaded media files with an AI model to create an output video.
- **Output Video Generation:** Save the generated video on the server and return a URL for easy access.
- **Scalable Design:** Built with Django and Django Rest Framework (DRF) for scalability and ease of extension.

## Technology Stack

- **Backend:** Django, Django Rest Framework (DRF)
- **AI Integration:** Custom AI model for processing media files
- **Storage:** Local file storage for media files and output videos

## Installation

### Prerequisites

- Python 3.x
- Django
- Django Rest Framework
- Any other dependencies required for your AI processing (e.g., OpenCV, TensorFlow)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/media-ai-processing-api.git
   cd media-ai-processing-api

2. Install Required Packages:
   ```bash
   pip install -r requirements.txt

3. Make migrations:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate

4. Start Development server:
   ```bash
   python manage.py runserver
