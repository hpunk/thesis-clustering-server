from flask import Flask,render_template,request, Response
from flask_migrate import Migrate
from sqlalchemy import func, create_engine
from myutils import distance_function, get_clustering_columns, generate_query_for_clustering
from sklearn.cluster import DBSCAN
from sklearn_extra.cluster import KMedoids
from sklearn import manifold
from scipy.spatial.distance import squareform
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/hello')
def hello_flask():
    df = pd.DataFrame(
        [["a", "b"], ["c", "d"]],
        index=["row 1", "row 2"],
        columns=["col 1", "col 2"],
    )
    return {'data' : json.loads(df.to_json(orient="records"))}

@app.route('/clustering/count', methods = ['GET'])
def count_data_to_cluster():
    state = request.args.get('st')
    province = request.args.get('pr')
    district = request.args.get('di')
    start_date = request.args.get('sd')
    end_date = request.args.get('ed')
    #connection
    engine = create_engine('postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local')
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    data_df = pd.read_sql_query(query,con=engine)
    return { 'count' : len(data_df['id']) }

@app.route('/clustering/hierarchical-to-scatter', methods = ['GET'])
def dendro_to_scatter():
    state = request.args.get('st')
    province = request.args.get('pr')
    district = request.args.get('di')
    start_date = request.args.get('sd')
    end_date = request.args.get('ed')
    k = request.args.get('k')
    #connection
    engine = create_engine('postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local')
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    #get data
    data_df = pd.read_sql_query(query,con=engine)
    data_to_cluster_df = data_df[get_clustering_columns()]
    data_matrix = data_to_cluster_df.values
    #distance vector
    vector_distance = []
    for i in range(len(data_matrix)):
        for j in range(i+1,len(data_matrix)):
            vector_distance.append(distance_function(data_matrix[i],data_matrix[j]))
    distance_matrix = squareform(vector_distance)
    #convert to array
    adist = np.array(distance_matrix)
    #we reduce dimentions to 3 for plotting
    mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
    results = mds.fit(adist)

    coords = results.embedding_
    
    labels = fcluster(Z, t=int(k), criterion='maxclust')
    str_labels = []
    for label in labels:
        str_labels.append(str(label))
    cluster_df = { 'x' : coords[:, 0], 'y' : coords[:, 1], 'z' : coords[:, 2], 'color': str_labels}
    df = pd.DataFrame(cluster_df)
    #scatterplot
    fig = px.scatter_3d(df, x='x', y='y', z='z', color='color')
    py.plot(fig, filename = "scatterplot_thesis", auto_open=False)
    #data to retrieve
    response_df = data_df.assign(label=labels)
    response_df = response_df.drop(['id'], axis = 1)

    unique_labels = list(set(labels))

    data = []
    for label in unique_labels:
        data.append({ 'group': str(label), 'data': json.loads(response_df[response_df['label']==label].to_json(orient="records")) })

    return {'response' : data}

    


@app.route('/clustering', methods = ['GET'])
def cluster_data():
    state = request.args.get('st')
    province = request.args.get('pr')
    district = request.args.get('di')
    start_date = request.args.get('sd')
    end_date = request.args.get('ed')
    algorithm = request.args.get('alg')
    k = request.args.get('k')
    mins = request.args.get('mins')
    eps = request.args.get('eps')
    #plotly
    username = "gustavo_alzamora_2021"
    apikey = "CSK3qWiFL9D29z8bjBLH"

    chart_studio.tools.set_credentials_file(username=username, api_key=apikey)
    #db connection
    engine = create_engine('postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local')
    query = generate_query_for_clustering(start_date,end_date,state,province,district)
    #extract data
    data_df = pd.read_sql_query(query,con=engine)
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
        clusters = KMedoids(n_clusters=int(k),metric=distance_function,random_state=0).fit(data_matrix) if algorithm=="0" else DBSCAN(min_samples=int(mins), metric=distance_function, eps=int(eps), p=1).fit(data_matrix)
        labels = clusters.labels_
        adist = np.array(distance_matrix)
        #dimention reduced to 3 for plotting
        mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
        results = mds.fit(adist)
        #plotting
        coords = results.embedding_
        str_labels = []
        for label in labels:
            str_labels.append(str(label))
        cluster_df = { 'x' : coords[:, 0], 'y' : coords[:, 1], 'z' : coords[:, 2], 'color':str_labels}
        df = pd.DataFrame(cluster_df)
        fig = px.scatter_3d(df, x='x', y='y', z='z', color='color')

        py.plot(fig, filename = "scatterplot_thesis", auto_open=False)
        #data to retrieve
        response_df = data_df.assign(label=labels)
        response_df = response_df.drop(['id'], axis = 1)

        unique_labels = list(set(labels))

        data = []
        for label in unique_labels:
            data.append({ 'group': str(label), 'data': json.loads(response_df[response_df['label']==label].to_json(orient="records")) })

        return {'response' : data}

    #hierarchical
    else:
        #clustering
        Z = linkage(vector_distance, 'average')
        #plotting
        fig = ff.create_dendrogram(Z)
        #dendrogram
        fig.update_layout(width=800, height=500)
        py.plot(fig, filename = "dendrogram_thesis", auto_open=False)
        #return value so front end can render dendrogram
        return { 'response' : 1 }

        
 
if __name__ == '__main__':
    app.run(debug=True)