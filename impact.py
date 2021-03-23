import pandas as pd
import numpy as np

# reading excel file
xls = pd.ExcelFile('Impacts from RFish 2019.xlsx')

# to read all sheets to a map
sheet_to_df_map = {}
for sheet_name in xls.sheet_names:
    sheet_to_df_map[sheet_name] = xls.parse(sheet_name)

# assingning each sheet to a dataFrame
df_collaboration = sheet_to_df_map['Collaborations']
df_influ_of_policy = sheet_to_df_map['Influence in Policy']
df_r_materials = sheet_to_df_map['Research Material']
df_r_databases = sheet_to_df_map['Research Databases']
df_i_property = sheet_to_df_map['Intellectual Property']
df_medical_pro = sheet_to_df_map['Medical Products']
df_artistic = sheet_to_df_map['Artistic']
df_software = sheet_to_df_map['Software']
df_recogntion = sheet_to_df_map['Recognition']
df_use_of_faci = sheet_to_df_map['Use of Facilities']



def find_impact(df): 
    '''takes a dataFrame as input, find the keywords and assign 0 or 1'''
    df_impact = df
    df_impact[['Patients, Cares, Patient Groups', 'General Public','Professional Practitioners','Policymaker']] = np.nan

    df_impact['Impact*'] = df_impact['Impact*'].str.lower()
    df_impact['Patients, Cares, Patient Groups'] = df_impact['Impact*'].str.contains('patient').astype(np.float).astype("Int32")
    df_impact['General Public'] = df_impact['Impact*'].str.contains('public').astype(np.float).astype("Int32")
    df_impact['Professional Practitioners'] = df_impact['Impact*'].str.contains('practioner').astype(np.float).astype("Int32")
    df_impact['Policymaker'] = df_impact['Impact*'].str.contains('policymaker').astype(np.float).astype("Int32")

    return df_impact

# 
df_collaboration = find_impact(df_collaboration)
df_influ_of_policy = find_impact(df_influ_of_policy)
df_r_materials = find_impact(df_r_materials)
df_r_databases = find_impact(df_r_databases)
df_i_property = find_impact(df_i_property)
df_medical_pro = find_impact(df_medical_pro)
df_artistic = find_impact(df_artistic)
df_software = find_impact(df_software)
df_recogntion = find_impact(df_recogntion)
df_use_of_faci = find_impact(df_use_of_faci)

# appending all dataFrame together
joined_df = df_collaboration.append([df_influ_of_policy, df_r_materials, df_r_databases, df_i_property, df_medical_pro, df_artistic, df_software, df_recogntion, df_use_of_faci], ignore_index = True)

# dropping all rows where impact is NaN
joined_df = joined_df[joined_df['Impact*'].notna()]

# converting to CSV
joined_df.to_csv('outputs\Impact.csv', encoding='utf-8', index=False)























































































































    # df_impact.loc['patient'.isin(df_impact['Impact*', 'Patients']), 'Patients'] = 1
    # df_impact.loc[~'patient'.isin(df_impact['Impact*', 'Patients']), 'Patients'] = 0




    
    # for i in range(len(df_impact['Impact*'])):
    #     if 'enable' in df_impact['Impact*'][i].lower():
    #         # print(df_impact['Patients'][i])
    #         df_impact = df_impact.Patients[i].replace(np.nan, 0)
    #         # print('True')
    #     else:
    #         # df_impact['Patients'][i] = 0
    #         # print(df_impact['Patients'][i])
    #         # df_impact.Patients[i] == 0
    #         df_impact = df_impact.Patients[i].replace(np.nan, 0)
            # print('F')
            #
            # df_impact.Patients['0']= 1
        # elif df["Impact*"].str.contains('Public').any():
        #     df_impact.Public['1']= 1
        # elif df_artistic["Impact*"].str.contains('Practioner').any():
        #     df_impact.Practioner['1']= 1
        # elif df["Impact*"].str.contains('Policymaker').any():
        #     df_impact.Policymaker['1']= 1