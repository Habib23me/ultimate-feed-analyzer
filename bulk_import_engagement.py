
from tqdm import tqdm
import pandas as pd
from services.database import ActivityUserDatabaseService

def dataLoader(path):
    data = pd.read_csv(path,encoding = "ISO-8859-1")
    return data

data=dataLoader("data/vibelikers.csv")
data.head()

# activityUserStore = ActivityUserStore()
for index, row in tqdm(data.iterrows(),bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}',total=len(data)):
    # au = ActivityUser(str(row['vibeId']), str(row['userId']), 1)
    # activityUserStore.putActivityUser(au)
    ActivityUserDatabaseService().put({
        "activityId":row['vibeId'],
        "userId":row['userId'],
        "score":1,
        },
        row['vibeId']+"_"+row['userId'])

    

aus = ActivityUserDatabaseService().get_all()

for au in aus:
    print(au.activity_id,  au.user_id, str(au.score))