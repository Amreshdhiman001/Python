import os
import requests
from datetime import datetime, timedelta
from github import Github

def get_pending_reviews(repo, days_threshold=2):
    pending_reviews = []

    for pull_request in repo.get_pulls(state='open'):
        if not pull_request.assignee:  # Exclude already assigned reviews
            last_updated = datetime.now() - pull_request.updated_at.replace(tzinfo=None)
            if last_updated.days >= days_threshold:
                pending_reviews.append(pull_request)

    return pending_reviews

def send_reminder(pending_reviews, repo, token):
    for pr in pending_reviews:
        reminder_comment = f"👋 Hey @{pr.user.login}! It's been ted. Could you please review it?"
        pr.create_issue_comment(reminder_comment)

def main(token):
    g = Github(token)
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

    # Customize the threshold based on your needs
    pending_reviews = get_pending_reviews(repo, days_threshold=2)

    if pending_reviews:
        send_reminder(pending_reviews, repo, token)

if __name__ == "__main__":
    main(os.environ['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'])
