Context
----------
This is code I wrote as a research assistant working with a large amount of Reddit data. The goal was to filter through the data if they mentioned certain key phrases such as "pensions" and map how coversations around the topic changed over time. As we were using university computers, not all Python packages were available to us.

FILTER_CODE.PY Description
----------
This code processes Reddit submissions and comments. It reads .zst files (searching by date). Then, it filters submissions by keyword and date range, finds related comments, and saves everything in a JSON structure. Comments include a reply level field.

Environment
----------
python/3.13.1
Required packages: `zstandard`, `json`, `argparse`, `datetime`, `os`, `re` (standard or install via pip as needed)

Running the Code
----------
The code can take 6 arguments:
-keyword= what keywords to search the Reddit posts for, enter as a comma separated list in quotations
-start_date= what date to begin searching for in the format YYYY-MM-DD
-end_date= what date to stop searching in the format YYYY-MM-DD
-sub_file= where the Reddit submission .zst are (defaults to /mnt/hum01-rds/YanWang/SocialCleavage/reddit/submissions/)
-com_file= where the Reddit submission .zst are (defaults to /mnt/hum01-rds/YanWang/SocialCleavage/reddit/comments/)
-output= output path

Example:
python3 structure_comments.py "pension, insurance" "2024-01-01" "2024-01-31" -- output /path/to/output/filtered_data.json

Running on CSF3 (SLURM)
------------------------
To run the script as a batch job on the CSF3 system:

1. Edit the `filter_comments.txt` SLURM script to add your command arguments
2. Submit using: sbatch filter_comments.txt

Output Structure
----------------
The resulting JSON file will contain a list of filtered Reddit submissions. Each submission includes:
- post_id
- post_url
- post_date
- post_title
- post_text
- comment_id
- comment_url
- comment_date
- comment_votes
- comment_body
- comment_has_multimedia
- comment_has_links
- number_of_replies
- reply_level: 1 for direct comments, 1+ for nested replies (Currently the code defaults to only preserving level 1 replies)

JSON_TO_CSV.PY Description
----------

This code turns the json file created above into a csv file with the headings: "post_id", "post_url", "post_date", "post_title", "post_text", "comment_id", "comment_url", "comment_date", "comment_votes", "comment_body", "comment_has_multimedia", "comment_has_links", "number_of_replies", "reply_level". 

Environment
----------
python/3.13.1
Required packages: `argparse` and `os` (standard or install via pip as needed)

Running the Code
----------
The code can take 2 arguments:
-path_to_json: path to the json file
-output_file: defaults to title of json file with csv at the end

Example:
python3 json_to_csv.py "/mnt/hum01-home01/n54183gd/reddit_post/results/sample_json.py"

This code can be run from the command line as it takes only a few seconds

SAMPLE_CSV.PY Description
----------

This code takes a random sample of the generated .csv file. 

Environment
----------
python/3.13.1
Required packages: `argparse` and `pandas` (standard or install via pip as needed)


Running 
-------
The code can take three arguments"
-csv_input= path to the input CSV file
-number= how many comments to return, defaults to 300 
-csv_output= name of the output csv file, defaults to 'random_sample.csv'

This code can be run from the command line as it takes only a few seconds

Example:
python3 random_sample.py "keywords_flat_output.csv"
