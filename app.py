from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', page_title='pagina inicial')

@app.route('/outra-pagina')
def outra_pagina():
    return render_template('outra_pagina.html', page_title='outra pagina')


if __name__ == '__main__':
    app.run(debug=True)
