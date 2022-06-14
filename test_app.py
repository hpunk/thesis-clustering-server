from fastapi.testclient import TestClient
from app import app
import pandas as pd
import json


client = TestClient(app)
max_number_cases = 380

#testing the hello URI
def test_hello_world():
    response = client.get('/hello')
    assert response.status_code == 200
    df = pd.DataFrame(
        [["a", "b"], ["c", "d"]],
        index=["row 1", "row 2"],
        columns=["col 1", "col 2"],
    )
    assert response.json() == {'data' : json.loads(df.to_json(orient="records"))}

#when using kmedoids algorithm for clustering, then receive the same amount of groups as the k parameter sent in the request
def test_clustering_kmedoids():
    cluster_number = 3
    response = client.get('/clustering?st=15&pr=1501&di=150103&sd=2017-01-01&ed=2017-01-31&alg=0&k='+str(cluster_number)+'&eps=0&mins=0')
    assert response.status_code == 200
    assert len(response.json()['response']) == cluster_number

#when using dbscan algorithm for clustering data, then receive the different groups and have a group with -1 representing the outliers if they are present
def test_clustering_dbscan():
    response = client.get('/clustering?st=15&pr=1501&di=150103&sd=2019-01-01&ed=2019-02-02&alg=1&eps=0.20&mins=5&k=0')
    assert response.status_code == 200
    assert len(response.json()['response']) == 3
    assert response.json()['response'][2]['group'] in ['Grupo 0','Grupo 1','Sin grupo']
    assert response.json()['response'][1]['group'] in ['Grupo 0','Grupo 1','Sin grupo']
    assert response.json()['response'][0]['group'] in ['Grupo 0','Grupo 1','Sin grupo']

#when using hierarchical approach to generate dendrogram, then only receive 1 as confirmation that the request has been succesfully handled
def test_clustering_hierarchical_dendrogram():
    response = client.get('/clustering?st=15&pr=1501&di=150103&sd=2019-01-01&ed=2019-01-15&alg=2&k=0&eps=0&mins=0')
    assert response.status_code == 200
    assert response.json()['response'] == 1

#when using hierarchical approach to generate scatter plot and send data, then the number of groups is the same as the one used in the request
def test_clustering_hierarchical_scatter():
    number_clusters = 3
    response = client.get('/clustering/hierarchical-to-scatter?st=15&pr=1501&di=150103&sd=2018-01-01&ed=2018-01-15&alg=2&k='+str(number_clusters))
    assert response.status_code == 200
    assert len(response.json()['response']) == number_clusters


#when number of cases to be clustered is greater than the max number of cases stated for a good performance, then a sampling is made
def test_sampling_of_clustering():
    count_response = client.get('/clustering/count?st=15&pr=1501&di=150103&sd=2020-01-01&ed=2020-03-30')
    data_response = client.get('/clustering?st=15&pr=1501&di=150103&sd=2020-01-01&ed=2020-03-30&alg=0&k=3&mins=0&eps=0')

    assert count_response.json()['count'] == 1020
    assert len(data_response.json()['response']) == 3
    data_response_json = data_response.json()
    assert len(data_response_json['response'][0]['data']) + len(data_response_json['response'][1]['data']) + len(data_response_json['response'][2]['data']) == max_number_cases

    data_response = client.get('/clustering/hierarchical-to-scatter?st=15&pr=1501&di=150103&sd=2020-01-01&ed=2020-03-30&alg=2&k=3')

    assert len(data_response.json()['response']) == 3
    data_response_json = data_response.json()
    assert len(data_response_json['response'][0]['data']) + len(data_response_json['response'][1]['data']) + len(data_response_json['response'][2]['data']) == max_number_cases