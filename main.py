from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_list():
    stories = read_data('database.csv')
    if request.method == "POST":
        return add_new_story()  # ha új story-t akarunk, megyünk a story page-re
    else:
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')  # egyébként táblázat megj


@app.route('/story', methods=['POST'])
def add_new_story():  # új story esetén átküld a form-ra egy üres 'story' listával
    return render_template('form.html', title='Add new Story', button='Create', story=['', '', '', '', '', '', ''])


@app.route('/list', methods=['POST'])
def Edit():
    stories = read_data('database.csv')  # beolvassuk a csv-t
    if request.form['button'] == 'Create':  # add new story esetén
        if len(stories) == 1:  # ha csak a címlista van
            id_number = '1'
        else:
            id_number = str(int(stories[len(stories)-1][0])+1)  # id = a felette lévő sor id-ja + 1
        new_row = []  # létrehozzuk az új sort
        new_row.append(id_number)
        new_row.append(request.form['story_title'])
        new_row.append(request.form['user_story'])
        new_row.append(request.form['criteria'])
        new_row.append(request.form['value'])
        new_row.append(request.form['estimation'])
        new_row.append(request.form['status'])
        stories = append_data(new_row)  # beletesszük a new_row listát a csv-be
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')
    elif request.form['button'] == 'Edit':  # edit esetén
        original_data = read_data()  # fogjuk az eredeti listát
        id = request.form['id']
        edit_row = []  # létrehozzuk az új edit-sort
        edit_row.append(id)
        edit_row.append(request.form['story_title'])
        edit_row.append(request.form['user_story'])
        edit_row.append(request.form['criteria'])
        edit_row.append(request.form['value'])
        edit_row.append(request.form['estimation'])
        edit_row.append(request.form['status'])
        new_data = []
        for row in original_data:
            if row[0] != id:  # a nem macerált id-jű sorokat betesszük a new datába
                new_data.append(row)
            else:
                new_data.append(edit_row)  # a maceráltat lecseréljük (id alapján)
        write_data(new_data)  # újraírjuk a csv-t a new datával
        return redirect('/')


@app.route('/edit/<id>')  # az edit tollacska ikonra kattintva
def edit(id):
    stories = read_data()  # fogjuk a táblázatot
    for row in stories:
        if row[0] == id:  # kiválasztjuk amelyiket editálni szeretnénk
            story = row  # az edit pagre a kiválasztott row listaelemeit rakjuk be (story=story)
    return render_template('form.html', title='Edit Story', button='Edit', story=story, id=id)


@app.route('/delete/<id>')  # ha a kis kukára kattintunk
def remove(id):
    original_data = read_data()
    new_data = []
    for row in original_data:
        if row[0] != id:  # a kiválasztott id-s storit nem rakjuk a new data-ba
            new_data.append(row)
    write_data(new_data)  # az id nélkül írjuk újra a fájlt
    return redirect('/')


def read_data(file_name='database.csv'):  # visszaadja a data listát, benne a sorokkal
    data = []
    with open(file_name, newline='') as file:
            datareader = csv.reader(file, delimiter=',', quotechar='|')
            for row in datareader:
                data.append(row)
    return data


def append_data(new_story, file_name='database.csv'):
    with open(file_name, 'a', newline='') as file:
        datawriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(new_story)  # hozzáadja a plusz sort
    stories = read_data('database.csv')
    return stories  # visszadja a listát


def write_data(story, file_name='database.csv'):  # a csv-be írja, amit máshol megadunk argumentként
    with open(file_name, 'w', newline='') as file:
        datawriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(story)


if __name__ == '__main__':
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
