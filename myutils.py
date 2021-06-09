import pandas as pd

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

def generate_df_with_labels(df,year):
    victim_aggr_link_labels = [] 
    violence_type_labels = []
    residence_area_labels = []
    aggr_lives_w_victim_labels = []
    victim_educ_level_labels = []
    enter_type_labels = []
    victim_civil_state_labels = []
    victim_ethnicity_labels = []
    date = []
    victim_sex = []
    aggr_sex = []

    sex_dict = {
        '0' : 'Mujer',
        '1' : 'Hombre'
    }

    val_dict = {
        '1': 'Vínculo Relacional de Pareja',
        '2': 'Vínculo Relacional Familiar',
        '3': 'Sin vínculo relacional de pareja ni familiar'
    }
    vcs_dict = {
        '1': 'Soltero/a',
        '2': 'Casado/a',
        '3': 'Divorciado/a',
        '4': 'Viudo/a'
    }

    ve_2017_dict = {
        '1': 'Quechua',
        '2': 'Aymara',
        '3': 'Nativo o indígena de la Amazonía',
        '4': 'Población afroperuana',
        '5': 'Blanco',
        '6': 'Mestizo',
        '7': 'Otra Etnia',
        '8': 'No sabe'
    }

    ve_2019_dict = {
        '1': 'Quechua',
        '2': 'Aimara',
        '3': 'Nativo o indígena de la amazonía',
        '4': 'Pueblo afroperuano',
        '5': 'Perteneciente de otro pueblo indígena u originario',
        '6': 'Blanco',
        '7': 'Mestizo',
        '8': 'Otro'
    }

    vt_dict = {
        '0': 'Violencia Económica-Patrimonial',
        '1': 'Violencia Psicológica',
        '2': 'Violencia Física',
        '3': 'Violencia Sexual'
    }

    ra_dict = {
        '0' : 'Rural',
        '1' : 'Urbano'
    }

    alwv_dict = {
        '1': 'Sí',
        '2': 'No',
        '3': 'De vez en cuando'
    }

    elv_2017_dict = {
        '1': 'Sin nivel',
        '2': 'Inicial',
        '3': 'Primaria Incompleta',
        '4': 'Primaria Completa',
        '5': 'Secundaria Incompleta',
        '6': 'Secundaria Completa',
        '7': 'Superior Técnico Incompleto',
        '8': 'Superior Técnico Completo',
        '9': 'Superior Universitario Incompleto',
        '10': 'Superior Universitario Completo'
    }

    elv_2018_dict = {
        '1': 'Sin nivel',
        '2': 'Inicial',
        '3': 'Primaria Incompleta',
        '4': 'Primaria Completa',
        '5': 'Secundaria Incompleta',
        '6': 'Secundaria Completa',
        '7': 'Superior Técnico Incompleto',
        '8': 'Superior Técnico Completo',
        '9': 'Superior Universitario Incompleto',
        '10': 'Superior Universitario Completo',
        '11': 'Básica Especial',
        '12': 'Maestría/Doctorado'
    }

    et_2017_dict = {
        '1': 'Acude directamente al servicio',
        '2': 'Acude al servicio por otro motivo',
        '3': 'Personal del CEM deriva el caso',
        '4': 'Ficha Notificación de Caso',
        '5': 'Ficha Línea 100',
        '6': 'Ficha Chat 100',
        '7': 'PNP',
        '8': 'Ministerio Público',
        '9': 'Poder Judicial',
        '10': 'SAU',
        '11': 'CAI',
        '12': 'Estrategia Rural'
    }

    et_2019_dict = {
        '1': 'Persona acude directamente al servicio',
        '2': 'Persona acude al servicio por otro motivo o solicita orientación por otras materias',
        '3': 'Personal de atención del CEM detecta e inserta el caso al servicio del CEM',
        '4': 'Personal de promoción del CEM detecta e inserta el caso al servicio del CEM',
        '5': 'Ficha de notificación de caso',
        '6': 'Ficha de derivación de Línea 100',
        '7': 'Ficha de derivación de Chat 100',
        '8': 'Ficha de derivación de CEM',
        '9': 'Derivado por la PNP',
        '10': 'Derivado por el Ministerio Público',
        '11': 'Derivado por el Poder Judicial',
        '12': 'Derivado por la UGEL o la DRE',
        '13': 'Servicio de Atención Urgente (SAU)',
        '14': 'Centro de Atención Institucional (CAI)',
        '15': 'Estrategia Rural (ER)'
    }

    et_2020_dict = {
        '1': 'Persona acude directamente al servicio',
        '2': 'Persona acude al servicio por otro motivo o solicita orientación por otras materias',
        '3': 'Personal de atención del CEM detecta e inserta el caso al servicio del CEM',
        '4': 'Personal de promoción del CEM detecta e inserta el caso al servicio del CEM',
        '5': 'Ficha de notificación de caso',
        '6': 'Ficha de derivación de Línea 100',
        '7': 'Ficha de derivación de Chat 100',
        '8': 'Derivado por la UGEL o la DRE',
        '9': 'Derivado por establecimiento de salud',
        '10': 'Derivado por la PNP',
        '11': 'Derivado por el Ministerio Público',
        '12': 'Derivado por el Poder Judicial',
        '13': 'Servicio de Atención Urgente (SAU)',
        '14': 'Centro de Atención Institucional (CAI)',
        '15': 'Estrategia Rural (ER)',
        '16': 'Ficha de CEM',
        '17': 'Ficha de EIU'
    }

    for i in range(len(df['cem'])):
        victim_aggr_link_labels.append(val_dict[str(int(df['victim_aggr_link'][i]))])
        victim_civil_state_labels.append(vcs_dict[str(int(df['victim_civil_state'][i]))])
        violence_type_labels.append(vt_dict[str(int(df['violence_type'][i]))])
        residence_area_labels.append(ra_dict[str(int(df['residence_area'][i]))])
        aggr_lives_w_victim_labels.append(alwv_dict[str(int(df['aggr_lives_w_victim'][i]))])
        victim_sex.append(sex_dict[str(int(df['victim_sex'][i]))])
        aggr_sex.append(sex_dict[str(int(df['aggr_sex'][i]))])
        date.append(str(df['case_date'][i]))
        if(year==2017):
            victim_ethnicity_labels.append(ve_2017_dict[str(int(df['victim_ethnicity'][i]))])
            victim_educ_level_labels.append(elv_2017_dict[str(int(df['education_level_victim'][i]))])
            enter_type_labels.append(et_2017_dict[str(int(df['enter_type'][i]))])
        elif(year==2018):
            victim_ethnicity_labels.append(ve_2017_dict[str(int(df['victim_ethnicity'][i]))])
            victim_educ_level_labels.append(elv_2018_dict[str(int(df['education_level_victim'][i]))])
            enter_type_labels.append(et_2017_dict[str(int(df['enter_type'][i]))])
        elif(year==2019):
            victim_ethnicity_labels.append(ve_2019_dict[str(int(df['victim_ethnicity'][i]))])
            victim_educ_level_labels.append(elv_2018_dict[str(int(df['education_level_victim'][i]))])
            enter_type_labels.append(et_2019_dict[str(int(df['enter_type'][i]))])
        elif(year==2020):    
            victim_ethnicity_labels.append(ve_2019_dict[str(int(df['victim_ethnicity'][i]))])
            victim_educ_level_labels.append(elv_2018_dict[str(int(df['education_level_victim'][i]))])
            enter_type_labels.append(et_2020_dict[str(int(df['enter_type'][i]))])

    return pd.DataFrame({
        '00_grupo' : df['label'],
        '01_fecha_caso' : date,
        '02_centro_emergencia_mujer' : df['cem'],
        '03_departamento' : df['state'],
        '04_provincia' : df['province'],
        '05_distrito' : df['district'],
        '06_sexo_victima' : victim_sex,
        '07_sexo_agresor' : aggr_sex,
        '08_vinculo_vict_agres' : victim_aggr_link_labels,
        '09_estado_civil_victima' : victim_civil_state_labels,
        '10_etnia_victima' : victim_ethnicity_labels,
        '11_victima_trabaja' : df['victim_works'],
        '12_nivel_educativo_victima' : victim_educ_level_labels,
        '13_victima_es_informante' : df['informant'],
        '14_agresor_vive_con_victima' : aggr_lives_w_victim_labels,
        '15_agresor_consumio_alcohol' : df['aggr_consume_alcoh'],
        '16_tipo_ingreso' : enter_type_labels,
        '17_numero_hijas' : df['daughters_number'],
        '18_numero_hijos' : df['sons_number'],
        '19_area_residencial' : residence_area_labels,
        '20_denuncia_registrada' : df['report_registered'],
        '21_edad_victima' : df['victim_age'],
        '22_tipo_violencia' : violence_type_labels,
        '23_hubo_agresion_economica' : df['economical_aggr'],
        '24_hubo_agresion_psicologica' : df['psychological_aggr'],
        '25_hubo_agresion_sexual' : df['sexual_aggr'],
        '26_hubo_agresion_fisica' : df['physical_aggr']
    })


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