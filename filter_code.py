import subprocess
import json
import os
import argparse
from datetime import datetime
import re
from collections import defaultdict

# Find relevant zst files
def find_matching_files(directory, years):
    return sorted([
        os.path.join(directory, fname)
        for fname in os.listdir(directory)
        if fname.endswith(".zst") and any(str(year) in fname for year in years)
    ])

# Filter submissions
def filter_posts(file_list, start_date, end_date, keywords):
    keyword_res = [re.compile(rf'\b{re.escape(k.lower())}\b') for k in keywords]
    filtered = {}

    for zst_path in file_list:
        process = subprocess.Popen(["zstd", "-dc", zst_path], stdout=subprocess.PIPE, universal_newlines=True)

        for line in process.stdout:
            try:
                post = json.loads(line)
                post_date = datetime.utcfromtimestamp(post.get("created_utc", 0))
                title = post.get("title", "").lower()
                selftext = post.get("selftext", "").lower()

                if start_date <= post_date <= end_date and any(k.search(title) or k.search(selftext) for k in keyword_res):
                    post_id = post["id"]
                    filtered[post_id] = {
                        "post_id": post_id,
                        "post_url": f"https://www.reddit.com{post.get('permalink', '')}",
                        "post_date": post_date.strftime("%Y-%m-%d"),
                        "post_title": post.get("title", "")
                    }
            except json.JSONDecodeError:
                continue

    return filtered

# Read relevant comments
def read_comments_from_files(file_list, post_dict):
    all_comments = []
    for zst_path in file_list:
        process = subprocess.Popen(["zstd", "-dc", zst_path], stdout=subprocess.PIPE, universal_newlines=True)

        for line in process.stdout:
            try:
                comment = json.loads(line)
                link_id = comment.get("link_id", "").split("_")[-1]
                if link_id in post_dict:
                    all_comments.append(comment)
            except json.JSONDecodeError:
                continue

    return all_comments

# Flatten nested comments
def build_flat_comments(comments, post_id):
    children = defaultdict(list)

    for comment in comments:
        if not isinstance(comment, dict):
            continue
        parent = str(comment.get("parent_id", "")).split("_")[-1]
        children[parent].append(comment)

    flat_list = []

    def assign_levels(parent_id, level):
        for child in children.get(parent_id, []):
            flat_list.append({
                "comment_id": child["id"],
                "comment_url": f"https://www.reddit.com{child.get('permalink', '')}",
                "comment_date": datetime.utcfromtimestamp(child.get("created_utc", 0)).strftime("%Y-%m-%d"),
                "comment_votes": child.get("score", 0),
                "comment_body": child.get("body", ""),
                "comment_has_multimedia": any(k in child.get("body", "").lower() for k in ["jpg", "png", "gif", "mp4", "youtube", "imgur"]),
                "comment_has_links": "http" in child.get("body", "").lower(),
                "number_of_replies": len(children.get(child["id"], [])),
                "reply_level": level
            })
            assign_levels(child["id"], level + 1)

    assign_levels(post_id, 1)
    return flat_list

# Main function
def main():
    parser = argparse.ArgumentParser(description="Filter Reddit posts and flatten comments.")
    parser.add_argument("keywords", help="Comma-separated list of keywords to search for in posts.")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--sub_dir", default="/mnt/hum01-rds/YanWang/SocialCleavage/reddit/submissions/", help="Submissions .zst folder")
    parser.add_argument("--com_dir", default="/mnt/hum01-rds/YanWang/SocialCleavage/reddit/comments/", help="Comments .zst folder")
    parser.add_argument("--output", default="/mnt/hum01-home01/n54183gd/reddit_post/results/keywords_flat_output.json", help="Output file path")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    years = {start_date.year, end_date.year}
    keywords = [kw.strip() for kw in args.keywords.split(",")]

    # Load relevant files
    sub_files = find_matching_files(args.sub_dir, years)
    com_files = find_matching_files(args.com_dir, years)

    # Filter posts
    post_dict = filter_posts(sub_files, start_date, end_date, keywords)

    if not post_dict:
        return

    # Read and flatten comments
    all_comments = read_comments_from_files(com_files, post_dict)

    for post_id in post_dict:
        relevant_comments = [c for c in all_comments if c.get("link_id", "").split("_")[-1] == post_id]
        flat_comments = build_flat_comments(relevant_comments, post_id)
        post_dict[post_id]["comments"] = flat_comments

    # Save output
    with open(args.output, "w") as f:
        json.dump(list(post_dict.values()), f, indent=2)

if __name__ == "__main__":
    main()
