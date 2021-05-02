import pandas as pd
import numpy as np
from recommendation import db
from recommendation.model.models import RecommendationDatasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation.exceptions import UnableToProvidedRecommendationAtThisTime

features = ['dept','thesis','specialization','interest1','interest2','interest3','interest4','internships','postMS']


class RecommendationEngine:
    def get_title_from_index(self,index):
        return self.df[self.df.index == index]

    def get_index_from_title(self,feature1,feature2="",feature3="",feature4="",feature5="",feature6=""):
        return self.df[((self.df.dept == feature1) & (self.df.thesis == feature2) & (self.df.specialization == feature3)) & (self.df.interest1 == feature4)].index.values

    def get_data_from_db(self):
        i = 0
        self.df = pd.DataFrame(columns = features)
        while True:
            data = RecommendationDatasets.query.filter_by(id=i+1).all()
            if not data:
                break
            data = str(data)[1:-1].split(",")
            self.df.loc[i] = data
            i += 1
        print (self.df)


    def combine_features(self,row):
        try:
            return row['dept'] +" "+row['thesis']+" "+row["specialization"]+" "+row["interest1"] +" "+row["interest2"] + " "+row["interest3"] + " "+row["interest4"] + row["internships"] + " "+row["postMS"]
        except:
            print ("Error:", row)

    def generateCosineSimilarity(self):
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(self.df)
        self.df["combined_features"] = self.df.apply(self.combine_features,axis=1)
        count_matrix = cv.fit_transform(self.df["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)
        return cosine_sim

    def getResults(self,feature1,feature2="",feature3="",feature4="",feature5="",feature6=""):
        self.get_data_from_db()
        cosine_sim = self.generateCosineSimilarity()
        course_index = self.get_index_from_title(feature1=feature1,feature2=feature2,feature3=feature3,feature4=feature4)
        if course_index.shape[0] == 0:
            raise UnableToProvidedRecommendationAtThisTime("Unable to provide recommendation at this time")
        print ("course_index",course_index)
        similar_courses =  list(enumerate(cosine_sim[course_index]))
        print ("similar_courses",similar_courses)
        sorted_similar_movies = sorted(similar_courses,key=lambda x:x[1][1],reverse=True)
        print ("sorted_similar_movies",sorted_similar_movies)
        for element in sorted_similar_movies:
            if element[0] in course_index:
                #print ("element",element[0])
                return element[0]

        return self.df[self.df.dept==feature1].index.values[0] or course_index[0]
