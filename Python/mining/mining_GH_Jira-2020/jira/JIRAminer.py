#! /usr/bin/python3
"""
Run this script with ./GHminer.py <Jira URL> <project names separated by comma - no space> <username> <password>
Saves  related variables for each issue in separate lines in a .csv..gz file
"""
import requests, sys, re, time, datetime, json, gzip
from jira import JIRA 
import pandas as pd 

def store_issues(allissues):
	issues = pd.DataFrame()
	for issue in allissues:
		try:
			d = {'key':      issue.key,
			'assignee name': [issue.fields.assignee.displayName if issue.fields.assignee is not None else ''][0],
			'assignee username': [issue.fields.assignee.name if issue.fields.assignee is not None else ''][0],
			'creator name' : [issue.fields.creator.displayName if issue.fields.creator is not None else ''][0],
			'creator username': [issue.fields.creator.name if issue.fields.creator is not None else ''][0],
			'reporter name': [issue.fields.reporter.displayName if issue.fields.reporter is not None else ''][0] ,
			'reporter username': [issue.fields.reporter.name if issue.fields.reporter is not None else ''][0],
			'created' : issue.fields.created,
			'components': ';'.join([x.name for x in issue.fields.components]),
			'description': [re.sub(r'\s+',' ',issue.fields.description.replace(',',';')) if issue.fields.description is not None else ''][0] ,
			'summary': [re.sub(r'\s+',' ',issue.fields.summary.replace(',',';')) if issue.fields.summary is not None else ''][0],
			'fixVersions': ';'.join([x.name for x in issue.fields.fixVersions]),
			'subtask': issue.fields.issuetype.subtask,
			'issuetype': issue.fields.issuetype.name,
			'priority': issue.fields.priority.name,
			'resolution': issue.fields.resolution,
			'resolution.date': issue.fields.resolutiondate,
			'status.name': issue.fields.status.name,
			'status.description': issue.fields.status.description,
			'updated': issue.fields.updated,
			# 'versions': ';'.join([x.name for x in issue.fields.versions]),
			'watches': issue.fields.watches.watchCount,
			'time spent' : issue.fields.timespent,
			'last viewed' : issue.fields.lastViewed,
			'project' : issue.fields.project.name
			}
			issues = issues.append(d, ignore_index=True)
		except Exception as e:
			sys.stderr.write(str(e))
	return issues 


def main(jiraobj, project):
	block_size = 1000
	block_num = 0
	allissues = []
	print ('Start getting issues for ', project)
	while True:
		start_idx = block_num*block_size
		print ('Getting block', block_num)
		issues = jiraobj.search_issues('project='+project, startAt=start_idx, maxResults=block_size)

		# break when all retrieved
		if len(issues) == 0: break

		block_num += 1
		allissues += issues
		# break
		time.sleep(1)

	print ('Retrieved', len(allissues), 'for project', project)
	data = store_issues(allissues)
	fname = project+'.csv.gz'
	data.to_csv(fname, encoding='utf-8', index = False, compression = 'gzip')
	print('completed writing issues for', project)


if __name__ == '__main__':
	if len (sys.argv) < 5:
		print ('Run with all Required Parameters')
		exit(1)
	else:
		projects = sys.argv[2].split(',')
		url = sys.argv[1]
		username = sys.argv[3]
		password = sys.argv[4]

		jiraobj = JIRA(url, basic_auth=(username, password))
		for project in projects:
			main(jiraobj, project)

