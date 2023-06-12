from flask import Flask,render_template,request
import pandas as pd

app = Flask(__name__)
record = []


@app.route('/')
def home():
    record.clear()
    data = pd.read_csv("https://assignment1m.blob.core.windows.net/assignment1/people.csv",usecols=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'])
    data['Salary'] = data['Salary'].fillna(0)
    dictn = data.to_dict(orient='records')
    for res in dictn:
        if res['Picture'] == ' ':
            res['Picture'] = res['Name']
            print(res['Picture'])

        if res['Salary'] == None or res['Salary'] == ' ':
            res['Salary'] = 0
        else:
            res['Salary'] = int(res['Salary'])
        record.append(res)

    return render_template('home.html',rec_res = record)


@app.route('/search',methods=['POST'])
def search():
    name_list = []
    pict = []

    if request.method == 'POST' and  request.form.get('Search_name') == 'Search Records':
        req = request.form
        for res in record:
                if res['Name'] == req['name']:
                    name_list.append(res)
                    print("length is {}" .format(len(res)))
        return render_template('home.html',rec_res =name_list)
    elif request.method == 'POST' and request.form.get('Search_pic') == 'Search picture for name':
        req = request.form
        name = ""
        for res in record:
            if res['Name'] == req['name']:
                name = res['Name']
                pict.append(res['Picture'])
        return render_template('search.html',rec_res = pict,name=name)

    elif request.method =='POST' and request.form.get('Search_pics') == 'Search Pictures':
        req = request.form
        # start and end value to the largest possible value of integer if users didnt enter any value
        strt_value = -(2**30)
        last_value = (2**30)
        if request.form.get('strt_value') != '':
            strt_value = int(req['strt_value'])

        if request.form.get('last_value') != '':
             last_value = int(req['last_value'])
        print(strt_value)
        for res in record:
            if res['Salary'] >= strt_value and res['Salary'] <= last_value :
                pict.append(res['Picture'])
        return render_template('search.html',rec_res =pict)


@app.route('/update',methods=['POST'])
def update():
    del_name = []
    img_name = []

    if request.method == 'POST' and request.form.get('delete_row') == 'Delete':
        for checkbox in request.form.getlist('check_box'):
            print(checkbox)
            del_name.append(checkbox)
        for res in list(record):
            if res['Name'] in del_name:
                record.remove(res)
        return render_template('home.html',rec_res = record)

    elif request.method == 'POST' and request.form.get('upload_image') == 'Upload image':
        print(request.form.get('image'))
        for checkbox in request.form.getlist('check_box'):
            img_name.append(checkbox)
        for res in record:
            if res['Name'] in img_name:
                res['Picture'] = request.form.get('image')
        return render_template('home.html',rec_res = record)

    elif request.method == 'POST' and request.form.get('update_val') == 'Update':
        return render_template('update.html',update_res = record)

@app.route('/update_list', methods = ['POST'])
def update_list():
    update_sal = []
    update_key = []
    indx = 0
    if request.method == 'POST' and request.form.get('update') == 'Update':
        for word in request.form.getlist('Salary'):
            print(f'word is {word}')
            update_sal.append(word)
        for word in request.form.getlist('Keywords'):
            print(f'word is {word}')
            update_key.append(word)

        for res in record:
            if res['Salary'] != update_sal[indx]:
                res['Salary'] = update_sal[indx]
            if res['Keywords'] != update_key[indx]:
                res['Keywords'] = update_key[indx]
            indx += 1
    return render_template('home.html', rec_res= record)


        

   



if __name__ == '__main__':
    app.run(debug=True)


