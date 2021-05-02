from flask import request

from recommendation import app, db
from recommendation.forms.forms import Validations
from recommendation.model.models import User , Dept, Specialization, Interests, PostMS, RecommendationDatasets
from recommendation.exceptions import EmailValidationError,UserNameValidationError,InvalidSessionID,InvalidDeptSelected,\
    InvalidSpecializationSelected,InvalidInterestSelected,InvalidPostMSOptionSelected,CourseNotSpecified,UnableToProvidedRecommendationAtThisTime
from recommendation.blogic.recommendation_engine import RecommendationEngine

import os
import redis
import uuid
import datetime
from bson import json_util
import json


redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

response_template = {
    'session_id':None,
    'response_code':200,
    'error_code':None,
    'data':None
    }

session_template = {
    'user_id':None,
    'username':None,
    'accessPermission':None,
    'email':None,
    'lastUpdatedSession':None,
    'lastServiceUsed':None
    }

db.create_all()

SERVICE_NAME = 'CourseRecommendation'
validationObj = Validations()
recommendationObj = RecommendationEngine()


def convert_to_db_class(data,feature):
    print ("data,feature",data,feature)
    if feature == "dept":
        if Dept.MSCEN_CS.value == data:
            return Dept.MSCEN_CS
        elif Dept.MSCEN_EE.value == data:
            return Dept.MSCEN_EE
        elif Dept.MSCS.value == data:
            return Dept.MSCS
        else:
            raise InvalidDeptSelected("Invalid Dept Selected")

    if feature == "specialization":
        if Specialization.general.value == data:
            return Specialization.general
        elif Specialization.cybersecurity.value == data:
            return Specialization.cybersecurity
        elif Specialization.bioinformatics.value == data:
            return Specialization.bioinformatics
        elif Specialization.bigdata.value == data:
            return Specialization.bigdata
        elif Specialization.asr.value == data:
            return Specialization.asr
        elif Specialization.cn.value == data:
            return Specialization.cn
        elif Specialization.ddss.value == data:
            return Specialization.ddss
        elif Specialization.msp.value == data:
            return Specialization.msp
        elif Specialization.vaes.value == data:
            return Specialization.vaes
        else:
            raise InvalidSpecializationSelected("Invalid Specialization Selected")

    if feature == "interest":
        if Interests.database.value == data:
            return Interests.database
        elif Interests.embedded.value == data:
            return Interests.embedded
        elif Interests.cloud.value == data:
            return Interests.cloud
        elif Interests.AI.value == data:
            return Interests.AI
        elif Interests.ML.value == data:
            return Interests.ML
        elif Interests.NLP.value == data:
            return Interests.NLP
        elif Interests.networking.value == data:
            return Interests.networking
        elif data == "":
            return ""
        else:
            raise InvalidInterestSelected("Invalid Interests selected")

    if feature == "postMS":
        if PostMS.undecided.value == data:
            return PostMS.undecided
        elif PostMS.work.value == data:
            return PostMS.work
        elif PostMS.research.value == data:
            return PostMS.research
        else:
            raise InvalidPostMSOptionSelected("Invalid PostMS option selected")



@app.route("/recommendation/getrecommendation", methods=['GET', 'POST'])
def getrecommendation():
    response = response_template.copy()

    try:
        session_id = request.headers.get('session_id',None)
        if not session_id:
            raise InvalidSessionID("Session does not exists")
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")

        dept = convert_to_db_class(request.form.get("dept"),"dept")
        thesis = "wanth" if request.form.get("thesis")=="True" else ""
        specialization = convert_to_db_class(request.form.get("specialization"),"specialization")

        interest1 = convert_to_db_class(request.form.get("interest1",""),"interest")
        interest2 = convert_to_db_class(request.form.get("interest2",""),"interest")
        interest3 = convert_to_db_class(request.form.get("interest3",""),"interest")
        interest4 = convert_to_db_class(request.form.get("interest4",""),"interest")
        internship = convert_to_db_class(request.form.get("internship",True),"internship")
        PostMS = convert_to_db_class(request.form.get("postMS","unde"),"postMS")

        if specialization:
            specialization = specialization.value
        if interest1:
            interest1 = interest1.value
        if interest2:
            interest2 = interest2.value
        if interest3:
            interest3 = interest3.value
        if interest4:
            interest4 = interest4.value

        print ("interest1",interest1,"interest2",interest2,"interest3",interest3,"interest4",interest4,"specialization",specialization)

        index = recommendationObj.getResults(feature1=dept.value,feature2=thesis,feature3=specialization,\
                                        feature4=interest1,feature5=interest2,feature6=interest3)


        data = RecommendationDatasets.query.filter_by(id=int(index)+1).first()
        courseTaken = data.courseTaken
        print ("courseTaken",courseTaken)
        courseTaken  = json.loads(courseTaken)
        response['response_code'] = 200
        response['data'] = courseTaken

    except UserNameValidationError:
        response['response_code'] = 406
        response['error_code'] = 11
    except EmailValidationError:
        response['response_code'] = 406
        response['error_code'] = 12
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    except InvalidDeptSelected:
        response['response_code'] = 406
        response['error_code'] = 15
    except InvalidSpecializationSelected:
        response['response_code'] = 406
        response['error_code'] = 16
    except InvalidInterestSelected:
        response['response_code'] = 406
        response['error_code'] = 17
    except InvalidPostMSOptionSelected:
        response['response_code'] = 406
        response['error_code'] = 18
    except UnableToProvidedRecommendationAtThisTime:
        response['response_code'] = 406
        response['error_code'] = 20
    return response




@app.route("/recommendation/giverecommendation", methods=['GET', 'POST'])
def giverecommendation():
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        if not session_id:
            raise InvalidSessionID("Session does not exists")
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")

        dept = convert_to_db_class(request.form.get("dept"),"dept")
        thesis = False if request.form.get("thesis")=="True" else False
        specialization = convert_to_db_class(request.form.get("specialization"),"specialization")
        interest1 = convert_to_db_class(request.form.get("interest1",""),"interest")
        interest2 = convert_to_db_class(request.form.get("interest2",""),"interest")
        interest3 = convert_to_db_class(request.form.get("interest3",""),"interest")
        interest4 = convert_to_db_class(request.form.get("interest4",""),"interest")
        internship = convert_to_db_class(request.form.get("internship",True),"internship")
        PostMS = convert_to_db_class(request.form.get("postMS","unde"),"postMS")
        courseTaken = request.form.get("courseTaken","")
        if not courseTaken:
            raise CourseNotSpecified("Couse Not Specified")

        courseTaken = json.loads(courseTaken)
        courseTaken = json.dumps(courseTaken)
        print ("interest1",interest1,"interest2",interest2,"interest3",interest3,"interest4",interest4)

        if interest3 and interest4:
            rec = RecommendationDatasets(dept=dept,thesis=thesis,specialization=specialization,interest1=interest1,interest2=interest2, \
                                         interest3=interest3,interest4=interest4,interships=internship,postms=PostMS,courseTaken=courseTaken)
        elif interest3:
            rec = RecommendationDatasets(dept=dept,thesis=thesis,specialization=specialization,interest1=interest1,interest2=interest2, \
                                         interest3=interest3,interships=internship,postms=PostMS,courseTaken=courseTaken)
        elif interest2:
            rec = RecommendationDatasets(dept=dept,thesis=thesis,specialization=specialization,interest1=interest1,interest2=interest2, \
                                         interships=internship,postms=PostMS,courseTaken=courseTaken)
        else:
            rec = RecommendationDatasets(dept=dept,thesis=thesis,specialization=specialization,interest1=interest1, \
                                         interships=internship,postms=PostMS,courseTaken=courseTaken)

        db.session.add(rec)
        db.session.commit()

        response['session_id'] = session_id
    except UserNameValidationError:
        response['response_code'] = 406
        response['error_code'] = 11
    except EmailValidationError:
        response['response_code'] = 406
        response['error_code'] = 12
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    except InvalidDeptSelected:
        response['response_code'] = 406
        response['error_code'] = 15
    except InvalidSpecializationSelected:
        response['response_code'] = 406
        response['error_code'] = 16
    except InvalidInterestSelected:
        response['response_code'] = 406
        response['error_code'] = 17
    except InvalidPostMSOptionSelected:
        response['response_code'] = 406
        response['error_code'] = 18
    except CourseNotSpecified:
        response['response_code'] = 406
        response['error_code'] = 19

    return response
