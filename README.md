# ExistentialRickBot

**[Dockerized](https://hub.docker.com/r/elucidation/existential_rick_bot/) and updated for PRAW4.3**

[/u/ExistentialRickBot](https://www.reddit.com/user/ExistentialRickBot/) is a [Reddit](http://www.reddit.com) Bot who finds meaning in life by listening to submissions on [/r/rickandmorty](https://www.reddit.com/r/rickandmorty/) subreddit and answering any questions as best it can.

## Meaning
The phrase "[Don't think about it](https://youtu.be/ItV8utelYlc)" is said by Rick in the Pilot episode of [Rick & Morty](https://en.wikipedia.org/wiki/Rick_and_Morty).


## Logic
The core logic is found on [lines ~41-44](existential_rick_bot.py#L41):

``` python
questions = ['why', 'happen', 'think?'] # Match if any of these are found in message
def isExistentialQuestion(message):
  return '?' in message and any([q in message.lower() for q in questions])

def getAnswerToExistentialQuestion():
  return "The answer is don't think about it."
```

ExistentialRickBot leaves a comment on such submissions, the response looks a bit like this:


The answer is don't think about it.

---

<sup>I am a bot | [`what is my purpose`](https://github.com/Elucidation/existential_rick_bot 'don't think about it')</sup>

## Developers
To set up praw credentials modify `example_praw.ini` with the correct credentials and rename the file to `praw.ini`.

One way to run this is to use `docker run elucidation/existential_rick_bot`.


## Feedback/Comments

Several options from low priority to high:
* Send a PM to ExistentialRickBot with comments.
* If there's an issue with a particular comment by ExistentialRickBot, please either reply to that comment with the issue and downvote as needed, I'll be adding auto-deletion if a comment goes negative.
* For software issues/suggestions/feature requests, create a new issue on this Github.
