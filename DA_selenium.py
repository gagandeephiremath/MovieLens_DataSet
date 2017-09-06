import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pandas import DataFrame 

driver = webdriver.Firefox()
driver.wait = WebDriverWait(driver, 30)
driver.get("https://grouplens.org/datasets/movielens/")

link = driver.find_element_by_link_text('ml-1m.zip')
link.click()
path = "/home/gagandeep/Downloads"
os.chdir(path)
time.sleep(30)
os.system("unzip ml-1m.zip -d ~/pistons/w2d3")

Unames = ['userId', 'gender', 'age', 'occupation', 'zip']
Users = pd.read_table('/home/gagandeep/pistons/w2d3/ml-1m/users.dat', sep='::', header=None, names=Unames, engine='python')
dFrame1 = DataFrame(Users, columns = ['userId', 'gender', 'age', 'occupation', 'zip'])
print(dFrame1)

Rnames = ['userId', 'movieId', 'rating', 'timestamp']
Ratings = pd.read_table('/home/gagandeep/pistons/w2d3/ml-1m/ratings.dat', sep='::', header=None, names=Rnames, engine='python')
dFrame2 = DataFrame(Ratings, columns=['userId', 'movieId', 'rating', 'timestamp'])
print(dFrame2)

Mnames = ['movieId', 'title', 'genres']
Movies = pd.read_table('/home/gagandeep/pistons/w2d3/ml-1m/movies.dat', sep='::', header=None, names=Mnames, engine='python')
dFrame3 = DataFrame(Movies, columns=['movieId','title','genres'])
print(dFrame3)


Data = pd.merge(pd.merge(Ratings,Users),Movies)
print("\n\nData after merging the entities\n\n")
dFrame4 = DataFrame(Data)
print(dFrame4[:10])

print("\n\nThe Information of the First User\n")
print(dFrame4.ix[0])

print("\n\nDataframe is empty??")
print(pd.isnull(dFrame4))


MeanRatings = Data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
MDframe = DataFrame(MeanRatings)
print(MDframe)

RatingsByTitle = dFrame4.groupby('title').size()
ActiveTitles = RatingsByTitle[RatingsByTitle > 300]
print(ActiveTitles)

MeanRatingsActive = MDframe.ix[ActiveTitles]
print("\n\nThe Mean of the active titles")
print(MeanRatingsActive)

TopFemaleRatings = MDframe.sort_index(by='F', ascending=False)
print("\n\nTop Female ratings\n\n", TopFemaleRatings[:15])

MDframe['diff'] = MDframe['M'] - MDframe['F']
SortedByDifference = MDframe.sort_index(by='diff')
print("\n\nThe Difference in agreement of wathching the movies", SortedByDifference[:15])

print("The Movies prefered by Men that were not rated by Women as highly\n\n", SortedByDifference[:-1][:15])
