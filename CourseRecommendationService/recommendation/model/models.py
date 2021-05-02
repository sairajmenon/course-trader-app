from recommendation import db
from datetime import datetime
import enum

class Dept(enum.Enum):
    MSCEN_CS = "mcecs"
    MSCEN_EE = "mceee"
    MSCS = "mscse"


class Specialization(enum.Enum):
    general = "gener"
    cybersecurity = "cserc"
    bioinformatics = "biome"
    bigdata = "bdata"
    asr = "robot"
    cn = "commn"
    ddss = "distr"
    msp = "multi"
    vaes = "vlsie"


class Interests(enum.Enum):
    database = "dbe"
    embedded = "ese"
    cloud = "cld"
    AI = "aie"
    ML = "mle"
    NLP = "nlp"
    networking = "net"

class PostMS(enum.Enum):
    undecided = "unde"
    work = "work"
    research = "phds"



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isadmin = db.Column(db.Boolean(), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.isadmin}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Post('{self.username}',{self.title}', '{self.content}',{self.date_posted}')"

class RecommendationDatasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept = db.Column(db.Enum(Dept))
    thesis = db.Column(db.Boolean(), nullable=False,default=False)
    specialization = db.Column(db.Enum(Specialization))
    interest1 = db.Column(db.Enum(Interests),default=None)
    interest2 = db.Column(db.Enum(Interests),default=None)
    interest3 = db.Column(db.Enum(Interests),default=None)
    interest4 = db.Column(db.Enum(Interests),default=None)
    interships = db.Column(db.Boolean(), nullable=True,default=True)
    postms = db.Column(db.Enum(PostMS),default=PostMS.work)
    courseTaken = db.Column(db.Text,nullable=True)


    def __repr__(self):
        dept = self.dept.value
        specialization = self.specialization.value
        if self.interships:
            param = "wantsintern"
        else:
            param = ""

        if self.thesis:
            thesis = "wanth"
        else:
            thesis = ""
        if not self.interest1:
            interest1 = ""
        else:
            interest1 = self.interest1.value

        if not self.interest2:
            interest2 = ""
        else:
            interest2 = self.interest2.value
        if not self.interest3:
            interest3 = ""
        else:
            interest3 = self.interest3.value

        if not self.interest4:
            interest4 = ""
        else:
            interest4 = self.interest4.value

        return "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(dept,thesis,specialization,interest1,interest2,interest3,interest4,param,self.postms.value,self.courseTaken)
