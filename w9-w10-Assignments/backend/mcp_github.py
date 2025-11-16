import requests
from typing import Dict, Any

# Base Github API URL
GITHUB_API = "https://api.github.com"

def get_repo_activity(owner: str, repo: str) -> Dict[str, Any]:
    """Fetch commits, issues, and pull requests from a GitHub repo."""
    activity = {}
    
    # Fetch the commits
    commits_url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"
    commits_resp = requests.get(commits_url)
    if commits_resp.status_code == 200:
        commits_data = commits_resp.json()[:5] # last 5 commits
        activity["commits"] = [
            {
                "author": c["commit"]["author"]["name"],
                "message": c["commit"]["message"],
                "date": c["commit"]["author"]["date"]
            }
            for c in commits_data
        ]
    else:
        activity["commits_error"] = commits_resp.text
        
    # Fetch open issues
    issues_url = f"{GITHUB_API}/repos/{owner}/{repo}/issues?state=open"
    issues_resp = requests.get(issues_url)
    if issues_resp.status_code == 200:
        issues_data = [
            {
                "title": i["title"],
                "user": i["user"]["login"],
                "created_at": i["created_at"]
            }
            for i in issues_resp.json() if "pull_requests" not in i # exclude PRs
        ]
        activity["open_issues"] = issues_data[:5]
    else:
        activity["issues_error"] = issues_resp.text
    
    # Fetch pull requests
    prs_url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls?state=all"
    prs_resp = requests.get(prs_url)
    if prs_resp.status_code == 200:
        prs_data = prs_resp.json()[:5]
        activity["pull_requests"] = [
            {
                "title": p["title"],
                "user": p["user"]["login"],
                "state": p["state"],
                "created_at": p["created_at"],
            }
            for p in prs_data
        ]
    else:
        activity["prs_errors"] = prs_resp.text
        
    return activity