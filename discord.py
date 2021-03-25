import requests

DISCORD_WEBOOK = 'https://discord.com/api/webhooks/821818300375236649/IBAm26ViMbK5J99OKuvuYtePih30SROAZk_LVIqh4qmUpR0p3ST1HgsFIuePXhriP13L'

def send_discord(content):
  data = { 'content': content }
  result = requests.post(DISCORD_WEBOOK, json = data)
  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Payload delivered successfully, code {}.".format(result.status_code))