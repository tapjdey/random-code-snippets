# mining_GH_Jira

Re: Personal - A2711-S: Git Repository.

### Mining GitHub: In Folder GitHub

Extract commits from GitHub: GHminer.py -> saves commit JSON objects to commit_data\_|repo|.gz

Filter commits with the word "fix" in message: GH_data_process.py -> saves commit data in filtered_commit_data\_|repo|.csv.gz

### Mining JIRA: In Folder jira

Extract Issues from JIRA repo and get attributes for the issues -> saves output in |project|.csv.gz
