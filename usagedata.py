#!/usr/bin/env python
 
"""
Usage: usagedata [options] <file>...
 
Options:
  --version             show version number
  -h, --help            show this help message
  --session=SESSION     show only usage data for the given connection identifier
  --jira                output the usage data using jira table format
 
Example:
  $ ./usagedata --session=fa574f43 mic-appserver.log
"""
 
import docopt
import re
import datetime
 
REG_EX = re.compile(r".*##### UsageData \[session=(?P<session>.+), category=(?P<category>.+), action=(?P<action>.+), description=(?P<description>.*), timestamp=(?P<timestamp>.+)\]")
 
def extract_usage_data(file_name, connection_id):
    """Extract usage data dictionaries from the given log file"""
    with open(file_name) as log_file:
        for line in log_file:
            match = REG_EX.match(line)
        if match:
            usage_data = match.groupdict()
            if connection_id is None or connection_id == usage_data["session"]:
                    yield usage_data
 
def normalize_usage_data(usage_data):
    """Normalize the extracted usage data"""
    usage_data["description"] = usage_data["description"].replace("/", ".")
    usage_data["timestamp"] = convert_milliseconds(usage_data["timestamp"])
    return usage_data
 
def convert_milliseconds(milliseconds):
    """Convert the given java timestamp into python date time object"""
    return datetime.datetime.fromtimestamp(int(milliseconds[:10])).replace(microsecond=int(milliseconds[10:]) * 1000).isoformat()
 
def print_usage_data(callback, usage_data):
    callback(usage_data)
 
def jira_format(usage_data):
    print("|%s|%s|%s|%s|%s|" % (usage_data["session"], usage_data["category"], usage_data["action"], usage_data["description"], usage_data["timestamp"]))
 
def json_format(usage_data):
    print(usage_data)
 
def main():
    arguments = docopt.docopt(__doc__, version=1.0)
    connection_id = arguments["--session"]
    jira = arguments["--jira"]
    output_format = jira_format if jira else json_format
    file_names = arguments["<file>"]
    if jira:
        print("||session||category||action||description||timestamp||")
    for file_name in file_names:
        for usage_data in extract_usage_data(file_name, connection_id):
        print_usage_data(output_format, normalize_usage_data(usage_data));
 
if __name__ == '__main__':
    main()
