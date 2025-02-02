from flask import render_template
from flask import Flask
import attendance
import Virtual_WhiteBoard

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('student.html')

@app.route('/button1')
def button1():
    # add functionality for button 1 here
    attendance.attendance()
    return 'Button 1 clicked!'

@app.route('/button2')
def button2():
    # add functionality for button 2 here
    Virtual_WhiteBoard.board()
    return 'Button 2 clicked!'

if __name__ == '__main__':
    app.run(debug=True)
