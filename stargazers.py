#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import pandas as pd
from tqdm import tqdm
import sys

def get_stargazers(owner, repo, token):
	url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
	headers = {
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"token {token}"
	}
	stargazers = []
	page = 1

	while True:
		response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
		if response.status_code != 200:
			break
		data = response.json()
		if not data:
			break
		stargazers.extend(data)
		page += 1

	return stargazers

def fetch_user_details(users, token):
	url_template = "https://api.github.com/users/{}"
	headers = {
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"token {token}"
	}
	user_details = []

	for user in tqdm(users, desc="Fetching user details"):
		response = requests.get(url_template.format(user["login"]), headers=headers)
		if response.status_code < 400: # If success, then get some basic details
			user_data = response.json()
			user_details.append({
				"login": user["login"],
				"name": user_data.get("name"),
				"email": user_data.get("email"),
				"location": user_data.get("location"),
				"blog": user_data.get("blog")
			})

	return user_details

def main():
	if len(sys.argv) != 3:
		print("Usage: python script.py <owner/repo> <output_csv>")
		sys.exit(1)

	owner_repo = sys.argv[1]
	output_csv = sys.argv[2]

	try:
		with open("INSERT_TOKEN_HERE.txt", "r") as file:
			token = file.read().strip()
			assert(len(token))
	except FileNotFoundError:
		open("INSERT_TOKEN_HERE.txt", 'a').close()
		print("Token file not found.")
		sys.exit(1)
	except AssertionError, AttributeError:
		print("Token file is empty.")
		sys.exit(1)

	owner, repo = owner_repo.split('/')
	stargazers = get_stargazers(owner, repo, token)
	print(f"Number of stargazers found: {len(stargazers)}")

	user_details = fetch_user_details(stargazers, token)

	# Save to CSV
	df = pd.DataFrame(user_details)
	df.to_csv(output_csv, index=False)
	print(f"Stargazers details saved to {output_csv}")

if __name__ == "__main__":
	main()
