import time
from datetime import datetime

def getResponseFooter():
  return "\n\n---\n\n^(I am a bot | )[^(`what is my purpose`)](https://github.com/Elucidation/existential_rick_bot 'don't think about it')"

def generateResponseMessage(msg):
  return "{}{}".format(msg, getResponseFooter())

# Check if submission has a comment by this bot already
def previouslyRepliedTo(submission, me):
  for comment in submission.comments:
    if comment.author == me:
      return True
  return False


def waitWithComments(sleep_time, segment=60):
  """Sleep for sleep_time seconds, printing to stdout every segment of time"""
  print("\t%s - %s seconds to go..." % (datetime.now(), sleep_time))
  while sleep_time > segment:
    time.sleep(segment) # sleep in increments of 1 minute
    sleep_time -= segment
    print("\t%s - %s seconds to go..." % (datetime.now(), sleep_time))
  time.sleep(sleep_time)

def logMessage(submission, status=""):
  print("{} | {} {}: {}".format(datetime.now(), submission.id, status, submission.title.encode('utf-8')))