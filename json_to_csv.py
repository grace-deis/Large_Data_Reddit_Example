import json
import csv
import argparse
import os

def flatten_reddit_json_to_csv(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "post_id", "post_url", "post_date", "post_title", "post_text",
            "comment_id", "comment_url", "comment_date", "comment_votes",
            "comment_body", "comment_has_multimedia", "comment_has_links",
            "number_of_replies", "reply_level"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for post in data:
            # Clean post text too
            clean_post_text = post.get("post_text", "").replace("\n", " ").strip()
            for comment in post.get("comments", []):
              if comment.get("reply_level") == 1:
                clean_body = comment.get("comment_body", "").replace("\n", " ").strip()
                writer.writerow({
                    "post_id": post.get("post_id"),
                    "post_url": post.get("post_url"),
                    "post_date": post.get("post_date"),
                    "post_title": post.get("post_title", "").replace("\n", " ").strip(),
                    "post_text": clean_post_text,
                    "comment_id": comment.get("comment_id"),
                    "comment_url": comment.get("comment_url"),
                    "comment_date": comment.get("comment_date"),
                    "comment_votes": comment.get("comment_votes"),
                    "comment_body": clean_body,
                    "comment_has_multimedia": comment.get("comment_has_multimedia"),
                    "comment_has_links": comment.get("comment_has_links"),
                    "number_of_replies": comment.get("number_of_replies"),
                    "reply_level": comment.get("reply_level")
                })
def main():
    parser = argparse.ArgumentParser(description="Convert Reddit JSON to CSV")
    parser.add_argument("json_input", help="Path to the input JSON file")
    parser.add_argument(
        "--csv_output",
        help="Path to the output CSV file (default: same name with .csv)",
        default=None
    )
    args = parser.parse_args()

    json_path = args.json_input
    csv_path = args.csv_output if args.csv_output else os.path.splitext(json_path)[0] + ".csv"

    flatten_reddit_json_to_csv(json_path, csv_path)
    print(f"CSV file created at: {csv_path}")

if __name__ == "__main__":
    main()
