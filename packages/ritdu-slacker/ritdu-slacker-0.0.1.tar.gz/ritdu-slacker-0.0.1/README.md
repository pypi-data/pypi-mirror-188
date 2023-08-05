# ritdu-slacker
pip installable bin to interact with the Ringier SA internal interface for slack.

# Motivation
- Single implementation of a wrapper around our internal slack interface.

# Installation
```bash
$ pip install ritdu-slacker
```

# Usage
To send a message to a slack channel from within a thread:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update in progress" --thread-uuid "${thread_uuid}" --thread-broadcast
```

To replace a message send a new one with the same message-uuid:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update complete!" --message-uuid "${message_uuid}"
```

To send a message and file to a thread in a slack channel:
```bash
$ ritdu-slacker file --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Oops!" --file "/tmp/errorlog.txt" --thread-uuid "${thread_uuid}"
```
