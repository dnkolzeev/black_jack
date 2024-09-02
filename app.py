from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/submit', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return redirect(f"/thank_you?name={name}")
    return render_template('form.html')

@app.route('/thank_you')
def thank_you():
    name = request.args.get('name')
    return f"Thank you, {name}, for submitting the form!"

if __name__ == '__main__':
    app.run()
