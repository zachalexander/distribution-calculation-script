import pandas as pd
import numpy as np


#setting up the proper index in the open dataframe
idx1 = range(1,8) + [77,88]
idx2 = ['varname'] + range(1,8)

idx_list = [idx1, idx2]

#reading in the template file to provide list of variables for gpr, spr, or dpr
template = pd.read_csv('template.csv')
idx3 = template['varname']
template_2 = pd.DataFrame(index=idx3)

#pull in mean ratings from abs.csv
mean_ratings = pd.read_csv('abs_edited.csv')
mean_ratings = mean_ratings.transpose()
mean_ratings = mean_ratings[[0]]
mean_ratings.columns = ['mean rating']
#mean_ratings.to_csv('mean_ratings.csv')

#spr variables for distribution table, move this to a new file if possible...
spr_library = idx3

#reads the fdn.xl file
output = pd.read_csv('fdn_xl_edited.csv')


#----taking the information from fdnxl and creating distributions from responses----#

for i in idx_list:

	dist_count2 = pd.DataFrame(index=i)

	#loop through the array until the end of spr_library; creates a column for each item in array; groups and counts
	for var in spr_library:

	#makes sure the input from spr_library matches with output file
		if var in output.columns:
			dist_count = output.groupby(var).count()
			dist_count2[var]=dist_count['fdntext']
			#dist_count2.to_csv('initial.csv')

	#transposes sheet so variables are in first column and 1-7 are headers
	dist_count3 = dist_count2.transpose()
	#dist_count3.to_csv('first_first_look.csv')

	#adds a column and sums the counts of each row to create a sum column
	dist_count3['Sum'] = dist_count3.sum(axis=1)
	#dist_count3.to_csv('first_look.csv')

	#restructures dataframe to ensure format looks correct and transposes again to get ready for percent calculations
	dist_count4 = pd.DataFrame(dist_count3, columns=[1, 2, 3, 4, 5, 6, 7, 77, 88, 'Sum'])
	dist_count4.index.name = 'varname'
	#dist_count4.to_csv('second_look.csv')

	#pulls the sum column for later
	sums_sheet = pd.DataFrame(dist_count4[['Sum']])
	sums_sheet = sums_sheet.reset_index(level=None)
	sums_sheet = pd.DataFrame(sums_sheet[['varname', 'Sum']])
	sums_sheet.columns = ['varname', 'Sum']
	#sums_sheet.to_csv('sums.csv')

	#turns the counts into percentages and rounds to the thousandths place
	dist_count5 = dist_count2 / dist_count4['Sum']
	#dist_count5.to_csv('to_percents.csv')

	#transposes sheet so variables are in first column and 1-7 are headers
	dist_count7 = dist_count5.transpose()
	#dist_count7.to_csv('test.csv')

	#restructures dataframe again to ensure format looks correct with percentages
	dist_count8 = pd.DataFrame(dist_count7, columns=[1, 2, 3, 4, 5, 6, 7, 77, 88, 'Sum'])
	#dist_count8.to_csv('ready_for_idx.csv')


	#prints out the without_dkna.csv file when going through the loop
	if i == idx1:
		#dist_count8.to_csv('with_dkna.csv')
		dist_count11 = dist_count8

	#prints out the with_dkna.csv file when going through the loop	
	if i == idx2:
		dist_count8['varname'] = dist_count8.index
		#dist_count8.to_csv('without_dkna.csv')
		dist_count8 = dist_count8[['varname', 1, 2, 3, 4, 5, 6, 7]]

		#----joining data from both outputs into a csv file that will then be merged with template----#
		dist_count11['varname'] = dist_count11.index
		dist_count11 = dist_count11[['varname', 77, 88]]
		dist_count13 = pd.merge(dist_count8, dist_count11, how='inner', on='varname')
		dist_count13 = pd.merge(dist_count13, sums_sheet, how='inner', on='varname')
		dist_count13 = dist_count13.set_index('varname')

		#join mean ratings with the template
		template_mean = template.join(mean_ratings, on='varname', how='left')

		#basically vlookups values from joint file to the template file	
		dist_count9 = template_mean.join(dist_count13, on='varname', how='left')

		#prints out the updated template file with the distribution table values, ready for macro
		dist_count9.to_csv('use_for_macro.csv', index=False)
		print '\nRUN WAS SUCCESSFUL!'







