from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from tqdm import tqdm
import pandas as pd
import numpy as np
import joblib as joblib
import csv
from sklearn.metrics import silhouette_score
from db.ClusterFeatureStore import ClusterFeature, clusterFeatureStore
from db.ActivityClusterStore import ActivityCluster, ActivityClusterStore

def dataLoader(path):
    data = pd.read_csv(path,encoding = "ISO-8859-1")
    return data

def describe_cluster(words_list,model):
    labels=model.labels_
    clusters=pd.DataFrame(list(zip(words_list,labels)),columns=['title','cluster'])
    u_labels =  np.array(np.unique(labels), dtype=object)
    pd.options.display.max_rows = 4000   
    for i in u_labels:
      print(i)
      print(clusters.loc[clusters['cluster'] == i])
      print('\n')

def cluster_text(text,k):
    vectorizer = TfidfVectorizer(stop_words={'english'})
    X = vectorizer.fit_transform(text)
    model = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    joblib.dump(model, 'model.pkl')
    score = silhouette_score(X, model.labels_, metric='euclidean')
    print("Silhouette score: {:.2f}".format(score))
    # describe_cluster(text,model)
    
    return model

arrayOfWords=[];
def groupDataSet(df):
    df.fillna('', inplace=True)
    df = df.reset_index()  # make sure indexes pair with number of rows
  
    for index, row in tqdm(df.iterrows(),bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}',total=len(df)):
       # add the feature to the array if it has not been added yet case insensitive
         if row['feature'] not in arrayOfWords:
            arrayOfWords.append(row['feature'])
            # 1132
    return cluster_text(arrayOfWords,1132);

data=dataLoader("data/final_features.csv")
data.head()
model=groupDataSet(data)
# data=predictCluster("Head")
# print(data)

def write_to_csv(datas, path):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for i in range(0,len(datas)):
            data=datas[i]
            writer.writerow([i,','.join(data)])

out = []
for i in range(0,max(model.labels_)+1):
    out.append([])

for i in range(0,len(arrayOfWords)):
    out[model.labels_[i]].append(arrayOfWords[i])
for i in range(0,len(out)):
    for word in out[i]:
        feature=ClusterFeature(i,word)
        clusterFeatureStore.putClusterFeature(feature)

# print(out)
# # write_to_csv(out,"data/clusters.csv")

cfs = clusterFeatureStore.getAllClusterFeatures()
for cf in cfs:
    print(cf.clusterId,cf.feature) 

# for cf in cfs:
#     print(cf.clusterId,cf.feature)

# data=dataLoader("data/final_features.csv")
# data.head()
# # model=groupDataSet(data)
# # # data=predictCluster("Head")
# # # print(data)

# # data.head()
# # cfs = clusterFeatureStore.getAllClusterFeatures()
# # print (len(clusterFeatureStore.getAllClusterFeatures()))
# # data['cluster'] = data['feature'].apply(lambda x: clusterFeatureStore.getClusterIdForFeature(cfs, x))
# # data.to_csv("data/clusters.csv", index=False)

# # clusterFeatureStore.close()

# activityClusterStore = ActivityClusterStore()
# # for index, row in tqdm(data.iterrows(),bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}',total=len(data)):
# #     #create an activity cluster object
# #     ac = ActivityCluster(row["activity_id"], row['feature'], row['score'], row['cluster'])
# #     #add the activity cluster to the store
# #     activityClusterStore.putActivityCluster(ac)
# # activityClusterStore.close()


