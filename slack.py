import requests

url = 'https://hooks.slack.com/services/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'


def send_message(content):
  data = { 'text': content }
  result = requests.post(url, json = data)
  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Payload delivered successfully, code {}.".format(result.status_code))