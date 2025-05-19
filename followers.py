#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import pandas as pd
from tqdm import tqdm
import sys

def get_followers(username, token):
	url = f"https://api.github.com/users/{username}/followers"
	headers = {
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"token {token}"
	}
	followers = []
	page = 1

	while True:
		response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
		if response.status_code != 200:
			break
		data = response.json()
		if not data:
			break
		followers.extend(data)
		page += 1

	return followers

def fetch_user_details(users, token):
	url_template = "https://api.github.com/users/{}"
	headers = {
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"token {token}"
	}
	user_details = []

	for user in tqdm(users, desc="Fetching user details"):
		response = requests.get(url_template.format(user["login"]), headers=headers)
		if response.status_code < 400:
			user_data = response.json()
			user_details.append({
				"login": user["login"],
				"name": user_data.get("name", ""),
				"email": user_data.get("email", ""),
				"location": user_data.get("location", ""),
				"blog": user_data.get("blog", "")
			})

	return user_details

def main():
	if len(sys.argv) < 2:
		print("Usage 1: python followers.py <github_url_or_username>")
		print("Usage 2: python followers.py <github_url_or_username> <output_csv>")
		sys.exit(1)

	username = sys.argv[1]
	username = username.rstrip("/")
	username = username.split('/')[-1]
	
	if len(sys.argv) > 2:
		output_csv = sys.argv[2]
	else:
		output_csv = username + ".csv"

	if not any(output_csv.lower().endswith(s) for s in [".csv", ".txt"]):
		output_csv += ".csv"

	try:
		with open("INSERT_TOKEN_HERE.txt", "r") as file:
			token = file.read().strip()
			assert(len(token))
	except FileNotFoundError:
		open("INSERT_TOKEN_HERE.txt", 'a').close()
		print("Token file not found.")
		sys.exit(1)
	except (AssertionError, AttributeError):
		print("Token file is empty.")
		sys.exit(1)

	followers = get_followers(username, token)
	print(f"Number of followers found: {len(followers)}")

	user_details = fetch_user_details(followers, token)

	df = pd.DataFrame(user_details)
	df.to_csv(output_csv, index=False)
	print(f"Followers details saved to {output_csv}")

if __name__ == "__main__":
	main()
