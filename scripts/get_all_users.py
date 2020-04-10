from multiprocessing import Pool
import twint #twitter scrapping tool
import nest_asyncio #twint has dependency on this
import pandas as pd
import asyncio
import os

nest_asyncio.apply() #so that multiple requests can be made at the same time

def search_query(args):
    global participant_handles_df
    i, usernames = list(args.items())[0]
    print(i, "searching thread")

    user_client = twint.Config()
    user_client.Store_csv = True
    user_client.Hide_output = True
    user_client.Output = os.path.join("data/tmp", "users_parallel_"+str(i)+".csv")

    for j, user in enumerate(usernames):
        print(i, ">>>>>", j)
        user_client.Username = user
        twint.run.Lookup(user_client)

    print(i, "finished")

if __name__=="__main__":
    
    participant_handles_df = pd.read_csv('data/unique_users.csv', usecols=['username'])
    NUM_USERS = participant_handles_df.shape[0]

    print("number of unique users: ",NUM_USERS)

    NUM_THREAD = 10

    SLICE_SIZE = int(NUM_USERS/NUM_THREAD)

    pool = Pool(NUM_THREAD)
    pool.map(search_query, [{i:participant_handles_df.username[SLICE_SIZE*i:SLICE_SIZE*(i+1]} for i in range(NUM_THREAD)])