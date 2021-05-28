from flask import Flask,render_template,request, Response
from flask_migrate import Migrate
from models import db, ClusterData
from sqlalchemy import func, create_engine
from myutils import distance_function
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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
 
@app.route('/hello')
def hello_flask():
    df = pd.DataFrame(
        [["a", "b"], ["c", "d"]],
        index=["row 1", "row 2"],
        columns=["col 1", "col 2"],
    )
    return {'data' : json.loads(df.to_json(orient="records"))}

@app.route('/clustering/hierarchical-to-scatter', methods = ['POST'])
def dendro_to_scatter():
    state = request.args.get('st')
    province = request.args.get('pr')
    district = request.args.get('di')
    start_date = request.args.get('sd')
    end_date = request.args.get('ed')
    k = request.args.get('k')

    engine = create_engine('postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local')
    query = "SELECT * FROM public.clustering_data where "
    query += "case_date >= "+start_date+" and case_date < "+end_date+" "
    if(district!=0):
        query += " and district="+str(district)+" "
    elif(province!=0):
        query += " and province="+str(province)+" "
    elif(state!=0):
        query += " and state="+str(state)+" "

    data_df = pd.read_sql_query(query,con=engine)
    ids = data_df[['id']]
    data_to_cluster_df = data_df[[
            'informant',
            'enter_type',
            'victim_sex',
            'daughters_number',
            'sons_number',
            'victim_ethnicity',
            'residence_area',
            'victim_civil_state',
            'education_level_victim',
            'victim_works',
            'victim_aggr_link',
            'aggr_lives_w_victim',
            'aggr_sex',
            'report_registered',
            'violence_type',
            'aggr_consume_alcoh',
            'victim_age',
            'physical_aggr',
            'psychological_aggr',
            'economical_aggr',
            'sexual_aggr'
        ]]

    data_matrix = data_to_cluster_df.values

    vector_distance = []
    for i in range(len(data_matrix)):
        for j in range(i+1,len(data_matrix)):
            vector_distance.append(distance_function(data_matrix[i],data_matrix[j]))
    distance_matrix = squareform(vector_distance)

    adist = np.array(distance_matrix)

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

    username = "gustavo_alzamora_2021"
    apikey = "CSK3qWiFL9D29z8bjBLH"

    chart_studio.tools.set_credentials_file(username=username, api_key=apikey)

    #response = ClusterData.query.filter(ClusterData.state == state).filter(ClusterData.province == province).filter(ClusterData.case_date.between(start_date,end_date)).order_by(ClusterData.id.asc())

    engine = create_engine('postgresql://postgres:p0stgr3SQL,@localhost:5432/thesis_local')
    query = "SELECT * FROM public.clustering_data where "
    query += "case_date >= "+start_date+" and case_date < "+end_date+" "
    if(district!=0):
        query += " and district="+str(district)+" "
    elif(province!=0):
        query += " and province="+str(province)+" "
    elif(state!=0):
        query += " and state="+str(state)+" "

    data_df = pd.read_sql_query(query,con=engine)
    ids = data_df[['id']]
    data_to_cluster_df = data_df[[
            'informant',
            'enter_type',
            'victim_sex',
            'daughters_number',
            'sons_number',
            'victim_ethnicity',
            'residence_area',
            'victim_civil_state',
            'education_level_victim',
            'victim_works',
            'victim_aggr_link',
            'aggr_lives_w_victim',
            'aggr_sex',
            'report_registered',
            'violence_type',
            'aggr_consume_alcoh',
            'victim_age',
            'physical_aggr',
            'psychological_aggr',
            'economical_aggr',
            'sexual_aggr'
        ]]

    data_matrix = data_to_cluster_df.values

    vector_distance = []
    for i in range(len(data_matrix)):
        for j in range(i+1,len(data_matrix)):
            vector_distance.append(distance_function(data_matrix[i],data_matrix[j]))
    distance_matrix = squareform(vector_distance)

    #kmedoids and dbscan
    if(algorithm == "0" or algorithm == "1"):
        clusters = KMedoids(n_clusters=int(k),metric=distance_function,random_state=0).fit(data_matrix) if algorithm=="0" else DBSCAN(min_samples=int(mins), metric=distance_function, eps=int(eps), p=1).fit(data_matrix)
        labels = clusters.labels_
        adist = np.array(distance_matrix)

        mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
        results = mds.fit(adist)

        coords = results.embedding_
        str_labels = []
        for label in labels:
            str_labels.append(str(label))
        cluster_df = { 'x' : coords[:, 0], 'y' : coords[:, 1], 'z' : coords[:, 2], 'color':str_labels}
        df = pd.DataFrame(cluster_df)
        fig = px.scatter_3d(df, x='x', y='y', z='z', color='color')

        py.plot(fig, filename = "scatterplot_thesis", auto_open=False)

        response_df = data_df.assign(label=labels)
        response_df = response_df.drop(['id'], axis = 1)

        unique_labels = list(set(labels))

        data = []
        for label in unique_labels:
            data.append({ 'group': str(label), 'data': json.loads(response_df[response_df['label']==label].to_json(orient="records")) })

        return {'response' : data}


    #hierarchical
    else:
        Z = linkage(vector_distance, 'ward')
        fig = ff.create_dendrogram(Z)
        #dendrogram
        fig.update_layout(width=800, height=500)
        py.plot(fig, filename = "dendrogram_thesis", auto_open=False)

        return 1

        
 
if __name__ == '__main__':
    app.run(debug=True)