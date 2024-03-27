from flask import Blueprint, render_template,redirect,url_for,session,request
from app.database.models import db

main_bp = Blueprint('main_bp',__name__)



import json
import logging
import os
import sys
import time
from pathlib import Path
import requests

logging.basicConfig(stream=sys.stdout, level=logging.INFO,  # set to logging.DEBUG for verbose output
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# Your Speech resource key and region
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY", '77fbd8bb53c4456a892496b43b1c54b8')
SERVICE_REGION = os.getenv("SERVICE_REGION", "westeurope")

NAME = "Simple avatar synthesis"
DESCRIPTION = "Simple avatar synthesis description"

# The service host suffix.
SERVICE_HOST = "customvoice.api.speech.microsoft.com"


def submit_synthesis(speech,sittingStyle,speechType,videoFormat,language):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }

    payload = {
        'displayName': NAME,
        'description': DESCRIPTION,
        "textType": speechType,#SSML,#PlainText 
        'synthesisConfig': {
            "voice": language,
        },
        # Replace with your custom voice name and deployment ID if you want to use custom voice.
        # Multiple voices are supported, the mixture of custom voices and platform voices is allowed.
        # Invalid voice name or deployment ID will be rejected.
        'customVoices': {
            # "YOUR_CUSTOM_VOICE_NAME": "YOUR_CUSTOM_VOICE_ID"
        },
        "inputs": [
            {
                "text": speech,
            },
        ],
        "properties": {
            "customized": False, # set to True if you want to use customized avatar
            "talkingAvatarCharacter": "lisa",  # talking avatar character
            "talkingAvatarStyle": sittingStyle,  # talking avatar style, required for prebuilt avatar, optional for custom avatar
            "videoFormat": videoFormat,  # mp4 or webm, webm is required for transparent background
            "videoCodec": "vp9",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "transparent",
        }
    }

    response = requests.post(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch avatar synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return response.json()["id"]
    else:
        logger.error(f'Failed to submit batch avatar synthesis job: {response.text}')


def get_synthesis(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    video_link = ''
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.debug('Get batch synthesis job successfully')
        logger.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            video_link = response.json()["outputs"]["result"]
            logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
        return response.json()['status'],video_link
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')
  
  
def list_synthesis_jobs(skip: int = 0, top: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar?skip={skip}&top={top}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')


def convert_to_gesture_casual(text):
    text = text.replace("#GST01","<bookmark mark='gesture.numeric1-left-1'/>")
    text = text.replace("#GST02","<bookmark mark='gesture.numeric2-left-1'/>")
    text = text.replace("#GST03","<bookmark mark='gesture.numeric3-left-1'/>")
    text = text.replace("#GST04","<bookmark mark='gesture.thumbsup-left-1'/>")
    text = text.replace("#GST05","<bookmark mark='gesture.show-front-1'/>")
    text = text.replace("#GST06","<bookmark mark='gesture.show-front-2'/>")
    text = text.replace("#GST07","<bookmark mark='gesture.show-front-3'/>")
    text = text.replace("#GST08","<bookmark mark='gesture.show-front-4'/>")
    text = text.replace("#GST09","<bookmark mark='gesture.show-front-5'/>")
    text = text.replace("#GST10","<bookmark mark='gesture.think-twice-1'/>")
    text = text.replace("#GST11","<bookmark mark='gesture.show-front-6'/>")
    text = text.replace("#GST12","<bookmark mark='gesture.show-front-7'/>")
    text = text.replace("#GST13","<bookmark mark='gesture.show-front-8'/>")
    text = text.replace("#GST14","<bookmark mark='gesture.show-front-9'/>")
    return text
    
def convert_to_gesture_graceful(text):
    text = text.replace("#GST01","<bookmark mark='gesture.wave-left-1'/>")
    text = text.replace("#GST02","<bookmark mark='gesture.wave-left-2'/>")
    text = text.replace("#GST03","<bookmark mark='gesture.thumbsup-left'/>")
    text = text.replace("#GST04","<bookmark mark='gesture.show-left-1'/>")
    text = text.replace("#GST05","<bookmark mark='gesture.show-left-2'/>")
    text = text.replace("#GST06","<bookmark mark='gesture.show-left-3'/>")
    text = text.replace("#GST07","<bookmark mark='gesture.show-left-4'/>")
    text = text.replace("#GST08","<bookmark mark='gesture.show-left-5'/>")
    text = text.replace("#GST09","<bookmark mark='gesture.show-right-1'/>")
    text = text.replace("#GST10","<bookmark mark='gesture.show-right-2'/>")
    text = text.replace("#GST11","<bookmark mark='gesture.show-right-3'/>")
    text = text.replace("#GST12","<bookmark mark='gesture.show-right-4'/>")
    text = text.replace("#GST13","<bookmark mark='gesture.show-right-5'/>")
    return text

def convert_to_gesture_technical(text):
    text = text.replace("#GST01","<bookmark mark='gesture.wave-left-1'/>")
    text = text.replace("#GST02","<bookmark mark='gesture.wave-left-2'/>")
    text = text.replace("#GST03","<bookmark mark='gesture.show-left-1'/>")
    text = text.replace("#GST04","<bookmark mark='gesture.show-left-2'/>")
    text = text.replace("#GST05","<bookmark mark='gesture.point-left-1'/>")
    text = text.replace("#GST06","<bookmark mark='gesture.point-left-2'/>")
    text = text.replace("#GST07","<bookmark mark='gesture.point-left-3'/>")
    text = text.replace("#GST08","<bookmark mark='gesture.point-left-4'/>")
    text = text.replace("#GST09","<bookmark mark='gesture.point-left-5'/>")
    text = text.replace("#GST10","<bookmark mark='gesture.point-left-6'/>")
    text = text.replace("#GST11","<bookmark mark='gesture.show-right-1'/>")
    text = text.replace("#GST12","<bookmark mark='gesture.show-right-2'/>")
    text = text.replace("#GST13","<bookmark mark='gesture.show-right-3'/>")
    text = text.replace("#GST14","<bookmark mark='gesture.point-right-1'/>")
    text = text.replace("#GST15","<bookmark mark='gesture.point-right-2'/>")
    text = text.replace("#GST16","<bookmark mark='gesture.point-right-3'/>")
    text = text.replace("#GST17","<bookmark mark='gesture.point-right-4'/>")
    text = text.replace("#GST18","<bookmark mark='gesture.point-right-5'/>")
    text = text.replace("#GST19","<bookmark mark='gesture.point-right-6'/>")
    return text
    


def convert_to_ssml(text,language):
    if language == "en-US-JennyNeural":
       lang = "en-US"
    elif language == "bn-BD-NabanitaNeural":
       lang = "bn-BD"
    ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}">
                                    <voice name="{language}">{text}</voice></speak>'''
    return ssml


def convert_to_pitchs(text):
    text = text.replace('#PTCXL','<prosody pitch="x-low" rate="x-slow">')
    text = text.replace('#PTCL','<prosody pitch="low" rate="slow">')
    text = text.replace('#PTCM','<prosody pitch="medium" rate="medium">')
    text = text.replace('#PTCH','<prosody pitch="high" rate="fast">')
    text = text.replace('#PTCXH','<prosody pitch="x-high" rate="x-fast">')
    text = text.replace('#EPTC','</prosody>')
    return text 


@main_bp.route('/',methods=['GET','POST'])
def index():
    notdesign = False
    if notdesign:
        
        if request.method == "POST":
            text = request.form['text']
            style = request.form['style']
            videoFormat = request.form['videoFormat']
            speechType = request.form['speechType']
            language = request.form['selectLanguage']
            #print(f'{style} avatar giving {speechType} speech in {language} language')
            
            if speechType == 'SSML':
                if style == "casual-sitting":
                    text = convert_to_gesture_casual(text)
                elif style == "graceful-sitting":
                    text = convert_to_gesture_graceful(text)
                elif style == "technical-sitting":
                    text = convert_to_gesture_technical(text)
                text = convert_to_pitchs(text)
                text = convert_to_ssml(text,language)
            
            job_id = submit_synthesis(text,style,speechType,videoFormat,language)
            while True:
                status,video_link = get_synthesis(job_id)
                if status == 'Succeeded':
                    return render_template('index.html', output_url=video_link)
                elif status == 'Failed':
                    return "Batch avatar synthesis job failed"
                else:
                    time.sleep(5)
            
            return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

