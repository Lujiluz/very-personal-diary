from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URL = os.environ.get('MONGODB_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def getDiary():
    diaries = list(db.diary.find({}, {'_id': False}))    
    return jsonify({
        'diaries': diaries,
        'msg': 'Data fetched!'
    })

@app.route('/diary', methods=['POST'])
def saveDiary():
    title = request.form['title']
    description = request.form['description']    
    image_file = request.files['image']
    emotion_file = request.files['emotion']
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    image_file_name = f'file-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg'
    emotion_file_name = f'emotion-file-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg'
    image_file.save(f'static/{image_file_name}')
    emotion_file.save(f'static/{emotion_file_name}')
    
    print(image_file.filename.split('.')[-1])
    data = {
        'title': title,
        'description': description,
        'image': image_file_name,
        'emotion': emotion_file_name,
        'date': current_date
    }
    
    db.diary.insert_one(data)
    return jsonify({'msg': 'Upload completed!'})



# function buat hapus file gambar dan emoticon di static
def deleteFile(directory, word_contain):
    # iterasi directory-nya
    for fileName in os.listdir(directory):
        # cek kalo nama kata yang dicari itu ada di nama file-nya
        if word_contain in fileName:
            # join directory sama filename buat dihapus
            filePath = os.path.join(directory, fileName)
            # cek lagi apakah file-nya beneran ada
            if os.path.isfile(filePath):
                # hapus file
                os.remove(filePath)
                # print pesan file berhasil dihapus
                print(f'File deleted: {filePath}')

@app.route('/diary', methods=['DELETE'])
def deleteAllDiaries():
    deleteFile('./static/', 'file-')
    deleteFile('./static/', 'emotion-file-')
    db.diary.delete_many({})
    return jsonify({'msg': 'Diaries Deleted!'})

if(__name__ == '__main__'):
    app.run('0.0.0.0', port=3000, debug=True)