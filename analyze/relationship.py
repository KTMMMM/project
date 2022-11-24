import pandas as pd
from character.detect_shape import distance
import numpy as np

def combine_2rd_columns(col_1, col_2):
    # result = int(col_1)
    # if not pd.isna(col_2):
    #     result += "," + str(col_2)
    if not pd.isna(col_2):
        result = [float(col_1),float(col_2)]
    return result

def get_user_data(user_data):

    json_data = user_data.dict()
    user_data_list = json_data['coorperate']

    user_data_df = pd.DataFrame(user_data_list)
    user_data_df.sort_values('time')
    user_data_df["coord"] = user_data_df.apply(lambda x: combine_2rd_columns(x['x'], x['z']), axis=1)
    user_data_df = user_data_df.drop(['x', 'z'], axis=1)
    users = user_data_df.id.unique()
    log_Users = []
    for i in users:
        index_Dict = {}
        globals()['userid_{}'.format(i)] = user_data_df[user_data_df['id'] == '{}'.format(i)].drop(columns = "id",axis=1)
        globals()['userids_{}'.format(i)] = globals()['userid_{}'.format(i)]["coord"]
        time_Index = list(globals()['userid_{}'.format(i)]["time"])
        globals()['userid_{}'.format(i)] = pd.Series(globals()['userids_{}'.format(i)].values,index=time_Index).rename('{}'.format(i))
        log_Users.append('{}'.format(i))
        
    log_Table = pd.concat([globals()['userid_{}'.format(i)] for i in log_Users], axis=1)
    log_Table.fillna('No data',inplace=True)
    # print(log_Table)
    return log_Table

def user_relationship(user_data):
    log_df = get_user_data(user_data)
    user_columns = log_df.columns
    time_index_list = log_df.index
    for time_recorded in time_index_list:
        selected_df = log_df.loc[[time_recorded]]
        for target_user in range(len(user_columns)):
            for compare_user in range(len(user_columns)):
                if user_columns[target_user] == user_columns[compare_user]:   # 같은 유저일 경우 패스
                    pass
                else: #다른 유저끼리 비교 
                    target, compare = user_columns[target_user], user_columns[compare_user]
                    target_data = selected_df[target].values[0]
                    compare_data = selected_df[compare].values[0]
                    if target_data !="No data" and compare_data != "No data":
                        # print(target_data[0],compare_data[0])
                        # print("target :",target,"///",target_data," : ",type(target_data))
                        # print("compare :",compare,"///",compare_data," : ",type(compare_data))
                        print(target,"-",compare," distance :",distance(target_data,compare_data))
    return '작업중'