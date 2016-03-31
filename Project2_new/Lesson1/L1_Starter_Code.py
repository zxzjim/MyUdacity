
# coding: utf-8

# ## Load Data from CSVs

# In[1]:

import unicodecsv

## Longer version of code (replaced with shorter, equivalent version below)

# enrollments = []
# f = open('enrollments.csv', 'rb')
# reader = unicodecsv.DictReader(f)
# for row in reader:
#     enrollments.append(row)
# f.close()

with open('enrollments.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    enrollments = list(reader)
    
print enrollments[0]


# In[2]:

#####################################
#                 1                 #
#####################################

## Read in the data from daily_engagement.csv and project_submissions.csv 
## and store the results in the below variables.
## Then look at the first row of each table.

with open('daily_engagement.csv', 'rb') as ef:
    reader = unicodecsv.DictReader(ef)
    daily_engagement = list(reader)
    
print daily_engagement[0]

with open('project_submissions.csv', 'rb') as sf:
    reader = unicodecsv.DictReader(sf)
    project_submissions = list(reader)
    
print project_submissions[0]


# ## Fixing Data Types

# In[3]:

from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')
    
# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    
enrollments[0]


# In[4]:

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
daily_engagement[0]


# In[5]:

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

project_submissions[0]


# ## Investigating the Data

# In[6]:

from collections import defaultdict, Counter
#####################################
#                 2                 #
#####################################

## Find the total number of rows and the number of unique students (account keys)
## in each table.
tables = [enrollments, daily_engagement, project_submissions]
results = []
for table in tables:
    accounts = defaultdict(int)
    for row in table:
        if 'acct' in row:
            k = row['acct']
            if accounts[k]:
                accounts[k] += 1
            else:
                accounts[k] = 1
        elif 'account_key' in row:
            k = row['account_key']
            if accounts[k]:
                accounts[k] += 1
            else:
                accounts[k] = 1
    '''for k,v in accounts.iteritems():
        print len(table),k,v'''
    print len(table), len(accounts.items())
    results.append((len(table), len(accounts.items())))
print results[0][1]    


# ## Problems in the Data

# In[7]:

#####################################
#                 3                 #
#####################################

## Rename the "acct" column in the daily_engagement table to "account_key".

for row in daily_engagement:
    row['account_key'] = row['acct']
    del row['acct']


# In[8]:

print daily_engagement[-1]


# ## Missing Engagement Records

# In[9]:

#####################################
#                 4                 #
#####################################

## Find any one student enrollments where the student is missing from the daily engagement table.
## Output that enrollment.
def get_unique_account(data):
    unique_accounts = set()
    for row in data:
        unique_accounts.add(row['account_key'])
    return unique_accounts

#get sets with account keys
unique_enrollments = get_unique_account(enrollments)
unique_daily_engagement = get_unique_account(daily_engagement)

print len(unique_enrollments)
#print unique_enrollments
print len(unique_daily_engagement)
#print unique_daily_engagement

for enrollment_record in enrollments:
    if enrollment_record['account_key'] in unique_daily_engagement:
        next
    else:
        print "account key not found in the daily engagement records: ", enrollment_record


# ## Checking for More Problem Records

# In[10]:

#####################################
#                 5                 #
#####################################

## Find the number of surprising data points (enrollments missing from
## the engagement table) that remain, if any.

results = []
print "account key doesn't exist in daily engagement and the join_date != cancel_date: "
for enrollment_record in enrollments:
    if (enrollment_record['account_key'] not in unique_daily_engagement) and (enrollment_record['join_date'] != enrollment_record['cancel_date']):
        results.append(enrollment_record)
        print enrollment_record
    else:
        next


# ## Tracking Down the Remaining Problems

# In[11]:

# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
print "udacity test account keys: ", udacity_test_accounts


# In[12]:

# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data


# In[13]:

# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print "records now removed all the udacity accounts"
print "len of non_udacity_enrollments", len(non_udacity_enrollments)
print "len of non_udacity_engagement", len(non_udacity_engagement)
print "len of non_udacity_submissions", len(non_udacity_submissions)
print "These are the clean data to be processed in further steps"


# ## Refining the Question

# In[14]:

#####################################
#                 6                 #
#####################################

## Create a dictionary named paid_students containing all students who either
## haven't canceled yet or who remained enrolled for more than 7 days. The keys
## should be account keys, and the values should be the date the student enrolled.

paid_students = {}
for student in non_udacity_enrollments:
    #print student
    if student['days_to_cancel']>7 or student['days_to_cancel'] is None:
        #add new record or update to the latest record
        if student['account_key'] not in paid_students or student['join_date'] > paid_students[student['account_key']]:
            paid_students[student['account_key']] = student['join_date']
print len(paid_students)


# ## Getting Data from First Week

# In[15]:

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >=0


# In[16]:

#####################################
#                 7                 #
#####################################

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.

def remove_free_trail_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data


# In[17]:

#daily engagement records of paid students
paid_engagements = remove_free_trail_cancels(non_udacity_engagement)
print "len of paid_engagements:", len(paid_engagements)

#daily engagement records in the first week of paid students
paid_engagement_in_first_week = []
for engagement in paid_engagements:
    #paid_student = {account_key: join_date}
    join_date = paid_students[engagement['account_key']]
    if within_one_week(join_date, engagement['utc_date']):
        paid_engagement_in_first_week.append(engagement)
        
print "len of paid_engagement_in_first_week:", len(paid_engagement_in_first_week)
print paid_engagement_in_first_week[0]
print paid_engagement_in_first_week[1]
print paid_engagement_in_first_week[2]


# ## Exploring Student Engagement

# In[18]:

from collections import defaultdict

def group_data(data):
    grouped_data_by_account = defaultdict(list)
    for data_point in data:
        account_key = data_point['account_key']
        grouped_data_by_account[account_key].append(data_point)
    return grouped_data_by_account
        

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
engagement_by_account = group_data(paid_engagement_in_first_week)
print "len of daily engagement grouped by accounts {account:engagements[]}:", len(engagement_by_account)


# In[61]:

import datetime
# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes
    
print "len of total_minutes (in one day) summed up by account {account: sum of total_minutes_visited}:", len(total_minutes_by_account)

# refactored as a function below:

def sum_grouped_items(grouped_data, field_name):
    sumed_data = {}
    for k, v in grouped_data.items():
        total = []
#        print k,v
        for data_point in v: 
            if isinstance(data_point[field_name], datetime.datetime):
                if data_point['num_courses_visited'] > 0:
#                    print k, data_point[field_name]
                    total.append(data_point[field_name])
                else:
                    continue
            else:
                total.append(data_point[field_name])
#        print "total[]: ", total
        
        if len(total)!=0:
            if isinstance(total[0], datetime.datetime):
#                print max(total), min(total)
                sumed_data[k] = len(total)
            else:
                sumed_data[k] = sum(total)
        else:
            sumed_data[k] = 0
    return sumed_data

total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')

print total_minutes_by_account


# In[62]:

import numpy as np

# Summarize the data about minutes spent in the classroom
total_minutes = total_minutes_by_account.values() #only use the value (totla_minutes) in the dict
#print total_minutes
print 'Mean:', np.mean(total_minutes)
print 'Standard deviation:', np.std(total_minutes)
print 'Minimum:', np.min(total_minutes)
print 'Maximum:', np.max(total_minutes)

#refactored as a method:
def describe_data(data):
    print 'Mean:', np.mean(data)
    print 'Standard deviation:', np.std(data)
    print 'Minimum:', np.min(data)
    print 'Maximum:', np.max(data)
    print '\n'
    
print "\nDescribe [total_minutes] by accounts:"
describe_data(total_minutes_by_account.values())


# ## Debugging Data Analysis Code

# In[63]:

#####################################
#                 8                 #
#####################################

## Go through a similar process as before to see if there is a problem.
## Locate at least one surprising piece of data, output it, and take a look at it.


# ## Lessons Completed in First Week

# In[64]:

#####################################
#                 9                 #
#####################################

## Adapt the code above to find the mean, standard deviation, minimum, and maximum for
## the number of lessons completed by each student during the first week. Try creating
## one or more functions to re-use the code above.



lessons_by_account = defaultdict(list)
for engagement in paid_engagement_in_first_week:
    lessons_by_account[engagement['account_key']].append(engagement['lessons_completed'])

total_lessons_by_account = {}
for account, lessons in lessons_by_account.items():
    #print account, lessons
    total_lessons = 0
    for lesson in lessons:
        total_lessons += lesson
    #print account, total_lessons
    total_lessons_by_account[account] = total_lessons

total_lessons = total_lessons_by_account.values()
print "mean: ", np.mean(total_lessons)
print "std: ", np.std(total_lessons)
print "min: ", np.min(total_lessons)
print "max: ", np.max(total_lessons)
print '\n'

#refactored as below:
engagements_by_account = group_data(paid_engagement_in_first_week)
total_lessons_by_account = sum_grouped_items(engagements_by_account, 'lessons_completed')
describe_data(total_lessons_by_account.values())


# ## Number of Visits in First Week

# In[65]:

######################################
#                 10                 #
######################################

## Find the mean, standard deviation, minimum, and maximum for the number of
## days each student visits the classroom during the first week.
total_visits_by_accounts = sum_grouped_items(engagement_by_account, 'utc_date')
describe_data(total_visits_by_accounts.values())


# ## Splitting out Passing Students

# In[98]:

######################################
#                 11                 #
######################################

## Create two lists of engagement data for paid students in the first week.
## The first list should contain data for students who eventually pass the
## subway project, and the second list should contain data for students
## who do not.

subway_project_lesson_keys = ['746169184', '3176718735']

passing_engagements = []
non_passing_engagements = []
passed_accounts = set()

paid_submissions = remove_free_trail_cancels(non_udacity_submissions)
for submission in paid_submissions:
	if submission['lesson_key'] in subway_project_lesson_keys and (submission['assigned_rating'] == 'PASSED' or submission['assigned_rating'] == 'DISTINCTION'):
		passed_accounts.add(submission['account_key'])

print len(passed_accounts)
for engagement in paid_engagement_in_first_week:
    if engagement['account_key'] in passed_accounts:
        passing_engagements.append(engagement)
    else:
        non_passing_engagements.append(engagement)

print "number of passing_engagements:", len(passing_engagements)
print "number of non_passing_engagements", len(non_passing_engagements)
# print passing_engagements

# ## Comparing the Two Student Groups

# In[49]:

######################################
#                 12                 #
######################################

## Compute some metrics you're interested in and see how they differ for
## students who pass the subway project vs. students who don't. A good
## starting point would be the metrics we looked at earlier (minutes spent
## in the classroom, lessons completed, and days visited).

passing_engagements_by_account = group_data(passing_engagements)
non_passing_engagements_by_account = group_data(non_passing_engagements)

passing_total_minutes_visited = sum_grouped_items(passing_engagements_by_account, 'total_minutes_visited')
non_passing_total_minutes_visited = sum_grouped_items(non_passing_engagements_by_account, 'total_minutes_visited')
print 'passing_total_minutes_visited mean: ', np.mean(passing_total_minutes_visited.values())
print 'non_passing_total_minutes_visited mean: ', np.mean(non_passing_total_minutes_visited.values())


passing_total_lessons_completed = sum_grouped_items(passing_engagements_by_account, 'lessons_completed')
non_passing_total_lessons_completed = sum_grouped_items(non_passing_engagements_by_account, 'lessons_completed')
print 'passing_total_lessons_completed mean: ', np.mean(passing_total_lessons_completed.values())
print 'non_passing_total_lessons_completed mean: ', np.mean(non_passing_total_lessons_completed.values())

passing_total_days_visited = sum_grouped_items(passing_engagements_by_account, 'utc_date')
non_passing_total_days_visited = sum_grouped_items(non_passing_engagements_by_account, 'utc_date')
print 'passing_total_days_visited mean: ', np.mean(passing_total_days_visited.values())
print 'non_passing_total_days_visited mean: ', np.mean(non_passing_total_days_visited.values())
# ## Making Histograms

# In[50]:

######################################
#                 13                 #
######################################

## Make histograms of the three metrics we looked at earlier for both
## students who passed the subway project and students who didn't. You
## might also want to make histograms of any other metrics you examined.
import matplotlib.pyplot as plt
plt.hist(passing_total_minutes_visited.values())
plt.hist(non_passing_total_minutes_visited.values())
plt.show()

plt.hist(passing_total_lessons_completed.values())
plt.hist(non_passing_total_lessons_completed.values())
plt.show()

plt.hist(passing_total_days_visited.values())
plt.hist(non_passing_total_days_visited.values())
plt.show()

# ## Improving Plots and Sharing Findings

# In[51]:

######################################
#                 14                 #
######################################

## Make a more polished version of at least one of your visualizations
## from earlier. Try importing the seaborn library to make the visualization
## look better, adding axis labels and a title, and changing one or more
## arguments to the hist() function.
import seaborn as sns

plt.hist(passing_total_minutes_visited.values())
plt.hist(non_passing_total_minutes_visited.values())
plt.xlabel('total_minutes_visited')
plt.ylabel('number of students')
plt.show()

plt.hist(passing_total_lessons_completed.values())
plt.hist(non_passing_total_lessons_completed.values())
plt.xlabel('total_lessons')
plt.ylabel('number of students')
plt.show()

plt.hist(passing_total_days_visited.values(), bins=8)
plt.hist(non_passing_total_days_visited.values(), bins=8)
plt.xlabel('total_days_visited')
plt.ylabel('number of students')
plt.show()