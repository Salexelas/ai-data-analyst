import requests
import time

start = time.time()

r = requests.get("https://api.groq.com")

print("TIME:", time.time() - start)