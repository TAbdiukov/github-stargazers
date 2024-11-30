# github-stargazers
Python 3.13 – Github Stargazer Scraper

## Install

```
pip install -r requirements.txt
```

## Paste API token

* Obtain a classic Github API token [here](https://github.com/settings/tokens),
* Paste it as-is to `INSERT_TOKEN_HERE.txt`

## Usage

```
python stargazers <owner/repo> <output_csv>
```

For example,

```
python stargazers.py https://github.com/leafo/etlua etlua.txt
python stargazers.py pjsip/pjproject pjpList1.csv
python stargazers.py daboynb/playcurlNEXT next
```

----------------------------------
**Tim Abdiukov**
