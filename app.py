from flask import Flask, request,render_template
import pickle
songs=pickle.load(open('song.sav','rb'))
similarity=pickle.load(open('similarity.sav','rb'))
def recommend(song):
    index = songs[songs['Title']==song].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    #creating an array
    recommend_song_name=[]
    for i in distances[1:6]:
        song_id=songs.iloc[i[0]].Index
        recommend_song_name.append(songs.iloc[i[0]].Title)
        
    return recommend_song_name
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/recommendation',methods=['GET','POST'])
def recommendation():
    song_list=songs['Title'].values
    status=False
    if request.method=="POST":
        try:
            if request.form:
                songs_name=request.form["songs"]
                print(songs_name)
                recommend_song_name=recommend(songs_name)
                status=True
                return render_template("recommendation.html",songs_name=recommend_song_name,song_list=song_list,status=status)

        except Exception as e:
            error=  {'error': e}
            return render_template("recommendation.html",error=error,song_list=song_list,status=status)
    else:
        return render_template("recommendation.html",song_list=song_list,status=status)



    


if __name__=="__main__":
    app.debug=True
    app.run()