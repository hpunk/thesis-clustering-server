from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class ClusterData(db.Model):
    __tablename__ = 'clustering_data'
 
    id = db.Column(db.Numeric, primary_key = True)
    case_date = db.Column(db.Date)
    cem = db.Column(db.Text)
    state = db.Column(db.Numeric)
    province = db.Column(db.Numeric)
    district = db.Column(db.Numeric)
    informant = db.Column(db.Boolean)
    enter_type = db.Column(db.Numeric)
    victim_sex = db.Column(db.Numeric)
    daughters_number = db.Column(db.Numeric)
    sons_number = db.Column(db.Numeric)
    victim_ethnicity = db.Column(db.Numeric)
    residence_area = db.Column(db.Numeric)
    victim_civil_state = db.Column(db.Numeric)
    education_level_victim = db.Column(db.Numeric)
    victim_works = db.Column(db.Boolean)
    victim_aggr_link = db.Column(db.Numeric)
    aggr_lives_w_victim = db.Column(db.Numeric)
    aggr_sex = db.Column(db.Numeric)
    report_registered = db.Column(db.Boolean)
    violence_type = db.Column(db.Numeric)
    aggr_consume_alcoh = db.Column(db.Boolean)
    victim_age = db.Column(db.Numeric)
    physical_aggr = db.Column(db.Boolean)
    psychological_aggr = db.Column(db.Boolean)
    economical_aggr = db.Column(db.Boolean)
    sexual_aggr = db.Column(db.Boolean)

    def __repr__(self):
        return '<ClusterData %r, %r, %r>' % (self.id, self.state, self.province)