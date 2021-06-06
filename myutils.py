def get_clustering_columns():
    return [
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
        ]

def generate_query_for_clustering(start_date,end_date,state,province,district):
    query = "SELECT * FROM public.clustering_data where "
    query += "case_date >= '"+start_date+"' and case_date <= '"+end_date+"' "
    if(district!=0):
        query += " and district="+str(district)+" "
    elif(province!=0):
        query += " and province="+str(province)+" "
    elif(state!=0):
        query += " and state="+str(state)+" "
    query += " order by id"
    return query

def distance_function(caseA,caseB):
    columns = [
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
    ]

    column_index = {
        'informant' : 0,
        'enter_type' : 1,
        'victim_sex' : 2,
        'daughters_number' : 3,
        'sons_number' : 4,
        'victim_ethnicity' : 5,
        'residence_area' : 6,
        'victim_civil_state' : 7,
        'education_level_victim' : 8,
        'victim_works' : 9,
        'victim_aggr_link' : 10,
        'aggr_lives_w_victim' : 11,
        'aggr_sex' : 12,
        'report_registered' : 13,
        'violence_type' : 14,
        'aggr_consume_alcoh' : 15,
        'victim_age' : 16,
        'physical_aggr' : 17,
        'psychological_aggr' : 18,
        'economical_aggr' : 19,
        'sexual_aggr' : 20
    }
    weights = {
        'informant' : 1,
        'enter_type' : 3,
        'victim_sex' : 3,
        'daughters_number' : 1,
        'sons_number' : 1,
        'victim_ethnicity' : 2,
        'residence_area' : 1,
        'victim_civil_state' : 4,
        'education_level_victim' : 5,
        'victim_works' : 3,
        'victim_aggr_link' : 2,
        'aggr_lives_w_victim' : 1,
        'aggr_sex' : 1,
        'report_registered' : 1,
        'violence_type' : 5,
        'aggr_consume_alcoh' : 1,
        'victim_age' : 3,
        'physical_aggr' : 4,
        'psychological_aggr' : 4,
        'economical_aggr' : 4,
        'sexual_aggr' : 4
    }

    types = {
        'informant' : 'categorical',
        'enter_type' : 'categorical',
        'victim_sex' : 'categorical',
        'daughters_number' : 'ordinal',
        'sons_number' : 'ordinal',
        'victim_ethnicity' : 'categorical',
        'residence_area' : 'categorical',
        'victim_civil_state' : 'categorical',
        'education_level_victim' : 'categorical',
        'victim_works' : 'categorical',
        'victim_aggr_link' : 'categorical',
        'aggr_lives_w_victim' : 'categorical',
        'aggr_sex' : 'categorical',
        'report_registered' : 'categorical',
        'violence_type' : 'categorical',
        'aggr_consume_alcoh' : 'categorical',
        'victim_age' : 'ordinal',
        'physical_aggr' : 'categorical',
        'psychological_aggr' : 'categorical',
        'economical_aggr' : 'categorical',
        'sexual_aggr' : 'categorical'
    }

    ordinal_max = {
        'daughters_number' : 20,
        'sons_number' : 20,
        'victim_age' : 120
    }
    
    def ordinal(x,y,column):
        return abs(x-y)*weights[column]/ordinal_max[column]

    def categorical(x,y,column):
        if(x == y):
            return 0
        else:
            return 1*weights[column]
    
    totalWeights = 0
    for col in columns:
        totalWeights += weights[col]
        
    distance = 0
    
    for col in columns:
        if(types[col] == 'categorical'):
            distance += categorical(caseA[column_index[col]], caseB[column_index[col]],col)
        elif(types[col] == 'ordinal'):
            distance += ordinal(caseA[column_index[col]], caseB[column_index[col]],col)
    return distance/totalWeights