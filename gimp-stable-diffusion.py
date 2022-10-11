#!/usr/bin/python

# v1.1.2

import urllib2
import tempfile
import os
import base64
import json
import re
import ssl
import sched, time

from gimpfu import *

# https://replicate.com/stability-ai/stable-diffusion/versions/a9758cbfbd5f3c2094457d996681af52552901775aa2d6dd0b17fd15df959bef
MODEL_ID = "a9758cbfbd5f3c2094457d996681af52552901775aa2d6dd0b17fd15df959bef"

API_URL = "https://api.replicate.com/v1/"

INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"

# HEADER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
HEADER_USER_AGENT = "nomeata/gimp-stable-diffusion"

# check every 5 seconds
CHECK_WAIT = 5
checkMax = None
s = sched.scheduler(time.time, time.sleep)


initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))

def getImageData(image, drawable):
   pdb.file_png_save_defaults(image, drawable, initFile, initFile)
   initImage = open(initFile, "rb")
   encoded = base64.b64encode(initImage.read())
   return encoded

def img2img(image, drawable, useInit, guidanceScale, promptStrength, steps, seed, imageCount, prompt, token):
   data = {
      "prompt": prompt,
      "width": int(image.width),
      "height": int(image.height),
      "prompt_strength": float(promptStrength),
      "num_outputs": int(imageCount),
      "num_inference_steps": int(steps),
      "guidance_scale": float(guidanceScale),
   }

   if seed:
     data.update({"seed": int(seed)})

   if useInit:
     imageData = getImageData(image, drawable)
     data.update({"init_image": "data:image/png;base64," + imageData})

   request = {
     "version": MODEL_ID,
     "input": data
   }

   url = API_URL + "predictions"
   req_body = json.dumps(request)
   headers = {
     "Authorization": "Token " + token,
     "Content-Type": "application/json",
     "User-agent": HEADER_USER_AGENT
   }

   request = urllib2.Request(url=url, data=req_body, headers=headers)
   pdb.gimp_progress_set_text("Starting dreaming now...")

   response = urllib2.urlopen(request)
   handleStatus(response, token)

def handleStatus(response, token):
   data = response.read()
   #print(data)
   data = json.loads(data)

   pdb.gimp_progress_set_text("Status: " + data["status"])

   if data["status"] == "starting" or data["status"] == "processing":
      s.enter(CHECK_WAIT, 1, checkStatus, (data["urls"]["get"],token))
      s.run()
   elif data["status"] == "failed" or data["status"] == "canceled":
      pdb.gimp_message(data["error"])
   elif data["status"] == "succeeded":
       for image_url in data["output"]:
          pdb.gimp_progress_set_text("Downloading image")

          headers = {
            "Authorization": "Token " + token,
            "User-agent": HEADER_USER_AGENT
          }
          request = urllib2.Request(url=image_url, headers=headers)
          response = urllib2.urlopen(request)
          with open(generatedFile, mode="wb") as d:
            d.write(response.read())

          imageLoaded = pdb.file_png_load(generatedFile, generatedFile)
          pdb.gimp_display_new(imageLoaded)

          # The seed is only part of the log, so tricky to parse

          # # image, drawable, x, y, text, border, antialias, size, size_type, fontname
          # pdb.gimp_text_fontname(imageLoaded, None, 2, 2, str(image["seed"]), -1, TRUE, 12, 1, "Sans")
          #pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])


       if os.path.exists(initFile):
            os.remove(initFile)

       if os.path.exists(generatedFile):
            os.remove(generatedFile)

def checkStatus(url, token):
  headers = {
    "Authorization": "Token " + token,
    "User-agent": HEADER_USER_AGENT
  }
  request = urllib2.Request(url=url, headers=headers)
  response = urllib2.urlopen(request)
  handleStatus(response, token)

register(
   "replicate_img2img",
   "replicate_img2img",
   "replicate_img2img",
   "BlueTurtleAI, nomeata",
   "BlueTurtleAI, nomeata",
   "2022",
   "<Image>/AI/Replicate.com img2img",
   "*",
   [
      (PF_TOGGLE, "useInit", "Use init image", False),
      #(PF_SLIDER, "maskBrightness", "Inpainting\nMask Brightness", 1.0, (0.0, 1.0, 0.1)),
      #(PF_SLIDER, "maskContrast", "Inpainting\nMask Contrast", 1.0, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "guidanceScale", "Guidance Scale", 7.5, (0, 20, 0.5)),
      (PF_SLIDER, "promptStrength", "Prompt strength", 0.8, (0.0, 1.0, 0.1)),
      (PF_SLIDER, "steps", "Steps", 20, (10, 150, 1)),
      (PF_STRING, "seed", "Seed (optional)", ""),
      (PF_SLIDER, "imageCount", "Number of images", 1, (1, 4,1)),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "token", "replicate.com token", "")
   ],
   [],
   img2img
)

main()
