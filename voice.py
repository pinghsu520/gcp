#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import io
import sys
import os
import pprint
import json
import asyncio

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

pp = pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, default='', help="Input audio file for speech processing", required=True)
args = vars(parser.parse_args())

client = speech.SpeechClient()

def transcribe_file_with_diarization():
    audio = types.RecognitionAudio(uri=args['input'])
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=22050,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
        model='phone_call'
    )

    operation = client.long_running_recognize(config, audio)
    print("Waiting on response from google cloud...")
    response = operation.result(timeout=720)  ## 360 call 01
    for result in response.results:
        print("\n\n::BEGIN TRANSCRIPT::\n")
        print("{}".format(result.alternatives[0].transcript))
        print("\n::END TRANSCRIPT::\n\n")

        print("\t\tCONFIDENCE: {} \n\n".format(result.alternatives[0].confidence))
        print("::BEGIN SPEAKER DIARIZATION::\n")
        words_info = result.alternatives[0].words
        for word_info in words_info:
            print("{}: '{}'".format(word_info.speaker_tag, word_info.word))
        print("\n::END SPEAKER DIARIZATION")

def main():
    if('input' in args):
        transcribe_file_with_diarization()


def version_check():
    if((sys.version_info[0] >= 3) and (sys.version_info[1] >= 7)):
        return True
    return False


if(__name__ == "__main__"):
    if(not version_check()):
        print("Must use python version 3.7+")
        sys.exit(1)
    main()

