from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from myutils import distance_function, get_clustering_columns, generate_query_for_clustering, generate_df_with_labels
from sklearn.cluster import DBSCAN,AgglomerativeClustering
from sklearn_extra.cluster import KMedoids
from sklearn import manifold
from scipy.spatial.distance import squareform
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fclusterdata, fcluster
import json
import pandas as pd
import numpy as np


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

max_number_cases = 380
database_connection_string = 'postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local'

@app.get('/hello')
def hello_fastapi():
    df = pd.DataFrame(
        [["a", "b"], ["c", "d"]],
        index=["row 1", "row 2"],
        columns=["col 1", "col 2"],
    )
    return {'data' : json.loads(df.to_json(orient="records"))}

@app.get('/clustering/count')
def count_data_to_cluster(st: int, pr : int, di : int, sd : str, ed : str):
    state = st
    province = pr
    district = di
    start_date = sd
    end_date = ed
    #connection
    ssl_args = {'sslrootcert': './server-ca.pem', 'sslcert':'./client-cert.pem', 'sslkey':'client-key.pem'}
    engine = create_engine(database_connection_string, connect_args=ssl_args)
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    data_df = pd.read_sql_query(query,con=engine)
    return { 'count' : len(data_df['id']) }

@app.get('/clustering/hierarchical-to-scatter')
def dendro_to_scatter(st: int, pr : int, di : int, sd : str, ed : str, k : int):
    state = st
    province = pr
    district = di
    start_date = sd
    end_date = ed
    #connection
    ssl_args = {'sslrootcert': './server-ca.pem', 'sslcert':'./client-cert.pem', 'sslkey':'client-key.pem'}
    engine = create_engine(database_connection_string,connect_args=ssl_args)
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    

    #get data
    data_df = pd.read_sql_query(query,con=engine)
    if(len(data_df) > max_number_cases):
        data_df = data_df.sample(n=max_number_cases, ignore_index=True)
    data_to_cluster_df = data_df[get_clustering_columns()]
    data_matrix = data_to_cluster_df.values
    #distance vector
    vector_distance = []
    for i in range(len(data_matrix)):
        for j in range(i+1,len(data_matrix)):
            vector_distance.append(distance_function(data_matrix[i],data_matrix[j]))
    distance_matrix = squareform(vector_distance)
    #hc = AgglomerativeClustering(n_clusters= None, affinity = 'precomputed', linkage = 'average', distance_threshold=0.3)
    Z = linkage(vector_distance, 'average')
    #convert to array
    adist = np.array(distance_matrix)
    #we reduce dimentions to 3 for plotting
    mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
    results = mds.fit(adist)

    coords = results.embedding_
    #labels = fclusterdata(X = data_matrix, metric = distance_function, method = 'ward', t=k)
    labels = fcluster(Z, t=Z[len(Z)-k][2], criterion='distance')
    #labels = hc.fit(distance_matrix).labels_
    str_labels = []
    for label in labels:
        str_labels.append("Grupo "+str(label))
    
    cluster_df = { 'x' : coords[:, 0], 'y' : coords[:, 1], 'z' : coords[:, 2], 'color': str_labels}
    df = pd.DataFrame(cluster_df)
    #scatterplot
    fig = px.scatter_3d(df, x='x', y='y', z='z', color='color')
    fig.update_layout(title_text='Diagrama de dispersión para visualizar grupos encontrados')
    py.plot(fig, filename = "scatterplot_thesis", auto_open=False)

    #data to retrieve
    response_df = data_df.assign(label=labels)
    response_df = response_df.drop(['id'], axis = 1)
    response_df = generate_df_with_labels(response_df,int(start_date[0:4]))
    unique_labels = list(set(labels))

    data = []
    for label in unique_labels:
        data.append({ 'group': str(label), 'data': json.loads(response_df[response_df['00_grupo']==label].to_json(orient="records")) })

    return {'response' : data}

    


@app.get('/clustering')
def cluster_data(st: int, pr : int, di : int, sd : str, ed : str, k : int, mins : int, eps : float,alg : str):
    state = st
    province = pr
    district = di
    start_date = sd
    end_date = ed
    algorithm = alg

    #plotly
    username = "gustavo_alzamora_2021"
    apikey = "CSK3qWiFL9D29z8bjBLH"

    chart_studio.tools.set_credentials_file(username=username, api_key=apikey)
    #db connection
    ssl_args = {'sslrootcert': './server-ca.pem', 'sslcert':'./client-cert.pem', 'sslkey':'client-key.pem'}
    engine = create_engine(database_connection_string,connect_args=ssl_args)
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    #extract data
    data_df = pd.read_sql_query(query,con=engine)
    if(len(data_df) > max_number_cases):
        data_df = data_df.sample(n=max_number_cases, ignore_index=True)
    data_to_cluster_df = data_df[get_clustering_columns()]
    data_matrix = data_to_cluster_df.values
    #distance vector
    vector_distance = []
    for i in range(len(data_matrix)):
        for j in range(i+1,len(data_matrix)):
            vector_distance.append(distance_function(data_matrix[i],data_matrix[j]))
    distance_matrix = squareform(vector_distance)

    #kmedoids and dbscan
    if(algorithm == "0" or algorithm == "1"):
        #clustering
        clusters = KMedoids(n_clusters=int(k),metric=distance_function,random_state=0).fit(data_matrix) if algorithm=="0" else DBSCAN(min_samples=int(mins), metric=distance_function, eps=float(eps), p=1).fit(data_matrix)
        labels = clusters.labels_
        adist = np.array(distance_matrix)
        #dimention reduced to 3 for plotting
        mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
        results = mds.fit(adist)
        #plotting
        coords = results.embedding_
        str_labels = []
        for label in labels:
            if(label != -1):
                str_labels.append("Grupo "+str(label))
            else:
                str_labels.append("Sin grupo")
        cluster_df = { 'x' : coords[:, 0], 'y' : coords[:, 1], 'z' : coords[:, 2], 'color':str_labels}
        df = pd.DataFrame(cluster_df)
        fig = px.scatter_3d(df, x='x', y='y', z='z', color='color')
        fig.update_layout(title_text='Diagrama de dispersión para visualizar grupos encontrados')
        py.plot(fig, filename = "scatterplot_thesis", auto_open=False)
        #data to retrieve
        response_df = data_df.assign(label=labels)
        response_df = response_df.drop(['id'], axis = 1)
        response_df = generate_df_with_labels(response_df,int(start_date[0:4]))
        unique_labels = list(set(labels))

        data = []
        for label in unique_labels:
            data.append({ 'group': str(label), 'data': json.loads(response_df[response_df['00_grupo']==label].to_json(orient="records")) })

        return {'response' : data}

    #hierarchical
    else:
        #clustering
        Z = linkage(vector_distance, 'average')
        #plotting
        fig = ff.create_dendrogram(Z)
        #dendrogram
        #fig.update_layout({'width'=900, 'height'=800})
        py.plot(fig, filename = "dendrogram_thesis", auto_open=False)
        #return value so front end can render dendrogram
        return { 'response' : 1 }
    
