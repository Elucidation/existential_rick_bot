#!/usr/bin/python
# -*- coding: utf-8 -*-
# Finds submissions with questions in them and replies as Rick would
import praw
import collections
import os
import time
from datetime import datetime
from praw.helpers import submission_stream
import requests
import socket

import auth_config

#########################################################
# Setup

# Set up praw
existential_rick_bot = "ExistentialRickBot"
user_agent = existential_rick_bot + " finds submissions with questions in them and replies as Rick would. See https://github.com/Elucidation/existential_rick_bot"

# Login
r = praw.Reddit(user_agent=user_agent)

# Login old-style due to Reddit politics
r.login(auth_config.USERNAME, auth_config.PASSWORD, disable_warning=True)

# Get accessor to subreddit
subreddit = r.get_subreddit('rickandmorty')

# How many submissions to read from initially
submission_read_limit = 100

# Filename containing list of submission ids that 
# have already been processed, updated at end of program
processed_filename = "submissions_already_processed.txt"

#########################################################
# Helper Functions

questions = ['why', 'happen', 'think?'] # Match if any of these are found in message
def isExistentialQuestion(message):
  return '?' in message and any([q in message.lower() for q in questions])

def getAnswerToExistentialQuestion():
  return "The answer is don't think about it."

def getResponseFooter():
  return "\n\n---\n\n^(I am a bot | )[^(`what is my purpose`)](https://github.com/Elucidation/existential_rick_bot 'don't think about it')"

def waitWithComments(sleep_time, segment=60):
  """Sleep for sleep_time seconds, printing to stdout every segment of time"""
  print("\t%s - %s seconds to go..." % (datetime.now(), sleep_time))
  while sleep_time > segment:
    time.sleep(segment) # sleep in increments of 1 minute
    sleep_time -= segment
    print("\t%s - %s seconds to go..." % (datetime.now(), sleep_time))
  time.sleep(sleep_time)

def logInfoPerSubmission(submission, count, count_actual):
  if ((time.time() - logInfoPerSubmission.last) > 120):
    print("\n\t---\n\t%s - %d processed submissions, %d read\n" % (datetime.now(), count_actual, count))
    logInfoPerSubmission.last = time.time()
  try:
    print("#%d Submission(%s): %s" % (count, submission.id, submission))
  except UnicodeDecodeError as e:
    print("#%d Submission(%s): <ignoring unicode>" % (count, submission.id))


logInfoPerSubmission.last = time.time() # 'static' variable

def loadProcessed(processed_filename=processed_filename):
  if not os.path.isfile(processed_filename):
    print("%s - Starting new processed file" % datetime.now())
    return set()
  else:
    print("Loading existing processed file...")
    with open(processed_filename,'r') as f:
      return set([x.strip() for x in f.readlines()])

def saveProcessed(already_processed, processed_filename=processed_filename):
  with open(processed_filename,'w') as f:
    for submission_id in already_processed:
      f.write("%s\n" % submission_id)
  print("%s - Saved processed ids to file" % datetime.now())


#########################################################
# Main Script
# Track commend ids that have already been processed successfully

# Load list of already processed comment ids
already_processed = loadProcessed()
print("%s - Starting with already processed: %s\n==========\n\n" % (datetime.now(), already_processed))

count = 0
count_actual = 0
running = True

while running:
  # get submission stream
  try:
    submissions = submission_stream(r, subreddit, limit=submission_read_limit)
    # for each submission
    for submission in submissions:
      count += 1
      # print out some debug info
      logInfoPerSubmission(submission, count, count_actual)

      # Skip if already processed
      if submission.id in already_processed:
        continue
      
      # check if submission title is a question
      if isExistentialQuestion(submission.title):
        # generate response
        msg = "%s%s" % (getAnswerToExistentialQuestion(), getResponseFooter())
        # respond, keep trying till success
        while True:
          try:
            print("> %s - Adding comment to %s: %s" % (datetime.now(), submission.id, submission))
            submission.add_comment(msg)
            # update & save list
            already_processed.add(submission.id)
            saveProcessed(already_processed)
            count_actual += 1
            # Wait after submitting to not overload
            waitWithComments(300)
            break
          except praw.errors.AlreadySubmitted as e:
            print("> %s - Already submitted skipping..." % datetime.now())
            break
          except praw.errors.RateLimitExceeded as e:
            print("> {} - Rate Limit Error for commenting on {}, sleeping for {} before retrying...".format(datetime.now(), submission.id, e.sleep_time))
            waitWithComments(e.sleep_time)

  
  # Handle errors
  except (socket.error, requests.exceptions.ReadTimeout, requests.packages.urllib3.exceptions.ReadTimeoutError, requests.exceptions.ConnectionError) as e:
    print("> %s - Connection error, resetting accessor, waiting 30 and trying again: %s" % (datetime.now(), e))
    saveProcessed(already_processed)
    time.sleep(30)
    continue
  except Exception as e:
    print("Unknown Error, continuing after 30:",e)
    time.sleep(30)
    continue
  except KeyboardInterrupt:
    print("Exiting...")
    running = False
  finally:
    saveProcessed(already_processed)
    print("%s - Processed so far:\n%s" % (datetime.now(),already_processed))


print("%s - Program Ended. Total Processed Submissions (%d replied / %d read):\n%s" % (datetime.now(), count_actual, count, already_processed))
