from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from model.AutoEncoder import decoder
from model.Classification import c_model
from model.EncodeReader import text_reader, name_reader
from model.MF import MatrixFactorization

app = Flask(__name__)
# CORS(app, resource={r'*': {'origins': 'http://localhost:8081/api'}})
# cors = CORS(app, resources={r"/api/*": {"localhost:8000": "*"}})

## 00. Static Variables 읽어내기
encoded_imgs = text_reader("encoded_imgs.txt")
origin_imgs = text_reader("origin_imgs.txt")
scents_name = name_reader()

################################################################# 임시 !!
factor = {1:[0, 1, 2, 3], 2:[4, 5, 6],
          3:[7, 8, 9, 10, 11], 4:[12, 13, 14, 15],
          5:[16, 17, 18, 19], 6:[20, 21, 22, 23],
          7:[24, 25, 26, 27], 8:[28, 29, 30, 31]}
#################################################################
## 01. 최초 선호도 테스트
@app.route('/api/ml/result', methods=['POST'])
def get_result():
    ## >> input : preference="0.9;0.8 ..."  || a=[1, 3, 2 ...]
    params = request.get_json()
    choose = params['choose']
    preference = params['pastPreference']
    if preference == '':
        preference = np.full((1, 32), 0.001).tolist()
    else:
        preference = list(map(float, params['pastPreference'].split(';')))
    ############################## bias 수정 !!!!!!!
    for choice in choose:
        if choice == 1:
            for i in factor[choice]:
                preference[0][i] += 0.05
    ############################## bias 수정 !!!!!!!
    new_preference = ''
    for pre in preference[0]:
        new_preference += str(pre)
        new_preference += ';'
    result = {"preference": new_preference}
    ## >> output : '0.454984;0.49897;0.894723...'
    return jsonify(result)

## 02. 선호도 점수 출력
## 02-1-a. 향수 상세
@app.route('/api/ml/predict/detail', methods=['POST'])
def predict_detail():
    ## >> input : preference="0.9;0.8 ..."  || now_perfume=30
    params = request.get_json()
    preference = list(map(float, params['preference'].split(';')[:-1]))
    preference = np.array(preference).reshape(1, -1)
    now_perfume = params['nowPerfume']
    target_perfume = np.array(encoded_imgs[now_perfume]).reshape(1, -1)
    predict_rate = target_perfume.dot(preference.T)
    decoded_img_prefer = decoder.predict(preference)
    origin_target_perfume = np.array(origin_imgs[now_perfume]).reshape(1, -1)
    fav_notes = []
    wor_notes = []
    for i in range(len(decoded_img_prefer[0])):
        if 0.5 > origin_target_perfume[0][i]:
            continue
        if decoded_img_prefer[0][i] > 0.5:
            fav_notes.append(i)
        else:
            wor_notes.append(i)
    if predict_rate >= 5:
        predict_rate = 5.0
    result = {"predictRate": round(predict_rate[0][0], 1), "favNotes": list(map(str, fav_notes[:5])), "worNotes": list(map(str, wor_notes[:5]))}
    ######## string 으로 이름으로 보내기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return jsonify(result)

## 02-1-b. 향수 상세
@app.route('/api/ml/predict/detail/similar', methods=['POST'])
def predict_detail_similar():
    ## >> input : preference="0.9;0.8 ..."  || now_perfume=30
    params = request.get_json()
    now_perfume = params['nowPerfume']
    target_perfume = np.array(encoded_imgs[now_perfume]).reshape(1, -1)
    similar_perfumes = []
    for pi in range(1003):
        if pi == now_perfume:
            continue
        similar_perfumes.append((target_perfume.dot(np.array(encoded_imgs[pi]).reshape(-1, 1)).tolist()[0][0], pi))
    similar_perfumes.sort()
    temp = []
    for spi in similar_perfumes[:10]:
        temp.append(spi[1])
    result = {"similarPerfumes": temp}
    return jsonify(result)

## 02-2. want it
@app.route('/api/ml/predict/want', methods=['POST'])
def predict_want():
    ## >> input : preference="0.9;0.8 ..."  || wantit=[5, 3, 2, ...]
    params = request.get_json()
    preference = list(map(float, params['preference'].split(';')[:-1]))
    preference = np.array(preference).reshape(1, -1)
    wants = params['wantPerfume']
    answer_arr = []
    for now in wants:
        target_perfume = np.array(encoded_imgs[now]).reshape(1, -1)
        answer = target_perfume.dot(preference.T)[0][0]
        if answer > 5:
            answer = 5.0
        answer_arr.append({"predict":answer, "perfumeIndex":now})
    answer_arr.sort(key=lambda x : x["predict"], reverse=True)
    result_json = {"result" : []}
    for aaa in answer_arr:
        result_json["result"].append(aaa)
    print(result_json)
    return jsonify(result_json)

## 02-3. 전체
@app.route('/api/ml/predict/all', methods=['POST'])
def predict_all():
    ## >> input : preference="0.9;0.8 ..."
    params = request.get_json()
    preference = list(map(float, params['preference'].split(';')[:-1]))
    preference = np.array(preference).reshape(1, -1)
    answer_arr = []
    for i in range(1003):
        target_perfume = np.array(encoded_imgs[i]).reshape(1, -1)
        answer = target_perfume.dot(preference.T)[0][0]
        if answer > 5:
            answer = 5.0
        answer_arr.append({"predict": answer, "perfumeIndex": i})
    answer_arr.sort(key=lambda x: x["predict"], reverse=True)
    result_json = {"result": []}
    cnt = 0
    for aaa in answer_arr:
        if cnt == 30:
            break
        result_json["result"].append(aaa)
        cnt += 1
    print(result_json)
    ## >> output : [4.8, 233], [3.3, 10] ...
    return jsonify(result_json)

## 03. 선호도 업데이트
@app.route('/api/ml/update', methods=['POST'])
def update_preference():
    ## >> input : perfumes = [[향수idx, 평점], ... ]
    params = request.get_json()
    data = params['perfumes']
    pidx, prate = data[0]["perfumeIndex"], data[0]["rating"]
    R = [[prate]]
    input_vec = np.array(encoded_imgs[pidx]).reshape(1, -1)
    for i in range(1, len(data)):
        pidx, prate =data[i]["perfumeIndex"], data[i]["rating"]
        R.append([prate])
        input_vec = np.concatenate((input_vec, np.array(encoded_imgs[i]).reshape(1, -1)), axis=0)
    ##### 모델 변경 사항 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # factorizer = MatrixFactorization(input_vec, R, k=32, learning_rate=0.01, reg_param=0.01, epochs=500, verbose=True)
    # factorizer.fit()s
    # preference = factorizer.print_results()
    # result = ''
    # for pre in preference:
    #     result += str(pre)
    #     result += ';'
    ################ 임시 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    new_preference = "0.101;0.101;0.101;0.101;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;0.001;"
    ################ 임시 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ## >> output : '0.454984;0.49897;0.894723...'
    result = {"preference": new_preference}
    return jsonify(result)

## 04. 워드클라우드
@app.route('/api/ml/word', methods=['POST'])
def get_words():
    ## input : preference='0.92;0.83;...'
    params = request.get_json()
    preference = list(map(float, params['preference'].split(';')[:-1]))
    preference = np.array(preference).reshape(1, -1)
    decoded_preference = decoder(preference)[0].numpy().tolist()
    temp = []
    for i in range(len(decoded_preference)):
        temp.append((decoded_preference[i], i))
    temp.sort(reverse=True)
    print(temp)
    result_json = {"cloud" : []}
    for tpp in temp:
        result_json["cloud"].append({"word": str(tpp[1]), "weight":tpp[0]})
    ################################ string 으로 이름으로 보내기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return jsonify(result_json)

## 05. 탑노트와 선호 노트 정렬
@app.route('/api/ml/graph', methods=['POST'])
def get_note_graph():
    ## input : preference='0.92;0.83;...'
    params = request.get_json()
    preference = list(map(float, params['preference'].split(';')[:-1]))
    preference = np.array(preference).reshape(1, -1)
    decoded_preference = decoder(preference)[0]
    ##### 모델 변경 사항 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # top_res_idx = c_model.predict(decoded_preference).index(1)
    top_res_idx = 5
    ##### 모델 변경 사항 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # top_res = scents_name[0][top_res_idx]
    top_res = 'Vanilla'
    decoded_preference = decoder(preference)[0].numpy().tolist()
    note_sorted_idx = []
    ######## string 으로 이름으로 보내기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for i in range(len(decoded_preference)):
        note_sorted_idx.append((decoded_preference[i], str(i)))
    middle_note_sorted_idx = note_sorted_idx[:80]
    base_note_sorted_idx = note_sorted_idx[81:160]
    middle_note_sorted_idx.sort(reverse=True)
    base_note_sorted_idx.sort(reverse=True)
    # result = {"mainScent":top_res, "middleWeight":note_sorted_idx[:80], "baseWeight":note_sorted_idx[81:160]}
    result = {"mainScent":top_res, "middleWeight":[], "baseWeight":[]}
    for mnsi in middle_note_sorted_idx:
        mw, mi = mnsi
        result["middleWeight"].append({"word": mi, "weight": mw})
    for bnsi in base_note_sorted_idx:
        bw, bi = bnsi
        result["baseWeight"].append({"word": bi, "weight": bw})
    ################################ string 으로 이름으로 보내기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return jsonify(result)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False)

# if __name__ == '__main__':
#     app.run(host='localhost', port=5000, threaded=False)