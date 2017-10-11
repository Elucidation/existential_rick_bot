#!/usr/bin/env python
# ExistentialRickBot daemon
# Listens on rickandmorty subreddit for submissions that 
# Run with --dry to dry run without actual submissions
from __future__ import print_function
import praw
import requests
import socket
import time
from datetime import datetime
import argparse

from erb_helpers import *

def isExistentialQuestion(message):
  return '?' in message and any(
    [q in message.lower() for q in ['why', 'happen', 'think', 'season 4', 'season four']])

def getAnswerToExistentialQuestion():
  return "The answer is don't think about it."


def startStream(args):
  reddit = praw.Reddit('ERB') # client credentials set up in local praw.ini file
  erb = reddit.user.me() # ExistentialRickBot object
  subreddit = reddit.subreddit('rickandmorty')

  # Start live stream on all submissions in the subreddit
  for submission in subreddit.stream.submissions():
    
    # Check if submission passes requirements and wasn't already replied to
    if isExistentialQuestion(submission.title):
      if not previouslyRepliedTo(submission, erb):
        # Generate response
        response = generateResponseMessage(getAnswerToExistentialQuestion())

        # Reply to submission with response
        if not args.dry:
          logMessage(submission,"[REPLIED]")
          submission.reply(response)
        else:
          logMessage(submission,"[DRY-RUN-REPLIED]")

        # Wait after submitting to not overload
        waitWithComments(300)
      else:
        logMessage(submission,"[SKIP]") # Skip since replied to already

    else:
      logMessage(submission)
      time.sleep(1) # Wait a second between normal submissions


def main(args):
  running = True
  while running:
    try:
      startStream(args)
    except (socket.error, requests.exceptions.ReadTimeout,
            requests.packages.urllib3.exceptions.ReadTimeoutError,
            requests.exceptions.ConnectionError) as e:
      print(
        "> %s - Connection error, retrying in 30 seconds: %s" % (
        datetime.now(), e))
      time.sleep(30)
      continue
    except Exception as e:
      print("Unknown Error, attempting restart in 30 seconds:",e)
      time.sleep(30)
      continue
    except KeyboardInterrupt:
      print("Keyboard Interrupt: Exiting...")
      running = False
  print('Finished')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--dry', help='dry run (don\'t actually submit replies)',
                      action="store_true", default=False)
  args = parser.parse_args()
  main(args)
