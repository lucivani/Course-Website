from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'b24886407237c574f9c9357f212476704f8ce65f862fbfdf3e9c1a109e281dc8'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'Student'
    StuAcc=db.Column(db.String(32), primary_key=True)
    StuName=db.Column(db.String(64), nullable=False)
    password=db.Column(db.String(32), nullable=False)
    Assignments=db.relationship('Assignments', backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.StuAcc}')"

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    InsAcc=db.Column(db.String(32), primary_key=True)
    InsName=db.Column(db.String(64), nullable=False)
    password=db.Column(db.String(32), nullable=False)
    Feedbacks=db.relationship('Feedbacks', backref='receiver', lazy=True)

    def __repr__(self):
        return f"Instructor('{self.InsAcc}')"
        
class Assignments(db.Model):
    __tablename__= 'Assignments'
    AID=db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(32), nullable=False)
    Marks=db.Column(db.Integer, nullable=False)
    Submitted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    StuAcc = db.Column(db.String(32), db.ForeignKey('Student.StuAcc'), nullable=False)
    Remarks = db.relationship('Remarks', backref='assignment', lazy=True)

    def __repr__(self):
        return f"Assignments('{self.AID}', '{self.Name}')"
        
class Remarks(db.Model):
    __tablename__='Remarks'
    RID=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Status=db.Column(db.String(32), nullable=False)
    Reason=db.Column(db.Text, nullable=False)
    Submitted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    AID = db.Column(db.Integer, db.ForeignKey('Assignments.AID'), nullable=False)

    def __repr__(self):
        return f"Remarks('{self.RID}', '{self.Status}')"

class Feedbacks(db.Model):
    __tablename__='Feedbacks'
    FID=db.Column(db.Integer, primary_key=True, autoincrement=True)
    content=db.Column(db.Text, nullable=False)
    Question=db.Column(db.Integer, nullable=False)
    Title = db.Column(db.String(32), nullable=False)
    Submitted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    View = db.Column(db.Integer, nullable=False, default=0)
    InsAcc = db.Column(db.String(32), db.ForeignKey('Instructor.InsAcc'), nullable=False)

    def __repr__(self):
        return f"Assignments('{self.FID}', '{self.Question}')"

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if 'name' in session:
        flash('You are already logged in!')
        if session['type'] == 'student':
            # redirect to student account
            return redirect(url_for('index'))
        # redirect to instructor account
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('register.html')
    
    role = request.form['Role']
    username = request.form.get('Username')
    fullname = request.form.get('FullName')
    password = request.form.get('Password')
    confirmation = request.form.get('ConfirmPass')
        
    if Student.query.filter_by(StuAcc=username).first() or Instructor.query.filter_by(InsAcc=username).first():
        flash('Username has been used. Try other username!', 'ERROR')
        return render_template('register.html',)
    if password != confirmation:
        flash('Password is not identical. Please try again!', 'ERROR')
        return render_template('register.html')
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if role == 'RoleStudent':
        user = Student(StuAcc=username, StuName=fullname, password=hashed_password)
    else:
        user = Instructor(InsAcc=username, InsName=fullname, password=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    flash('Your ID has been added! Please Login.')
    return redirect(url_for('login'))

@app.route('/', methods = ['POST', 'GET'])
def login():
    if 'name' in session:
        flash('You are already logged in!')
        if session['type'] == 'student':
            # redirect to student account
            return redirect(url_for('index'))
        # redirect to instructor account
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('Username')
    password = request.form.get('Password')

    StuAcc = Student.query.filter_by(StuAcc=username).first()
    InsAcc = Instructor.query.filter_by(InsAcc=username).first()

    if not (StuAcc and bcrypt.check_password_hash(StuAcc.password, password)) and not (InsAcc and bcrypt.check_password_hash(InsAcc.password, password)):
        flash('Please check your login details and try again!', 'ERROR')
        return render_template('login.html')
    
    if StuAcc and bcrypt.check_password_hash(StuAcc.password, password):
        # redirect to student account
        session['name'] = username
        session['type'] = 'student'
        session.permanent = True
        return redirect(url_for('index')) # gantiiiiiiiiiiiiiiiii
    # redirect to instructor account
    session['name'] = username
    session['type'] = 'instructor'
    session.permanent = True
    return redirect(url_for('index'))

@app.route('/index')
def index():
    if not session.get('name'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('name', default=None)
    session.pop('type', default=None)
    flash('You were logged out!', 'login')
    return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')
    
@app.route('/assignment1')
def assignment1():
    return render_template('assignment1.html')

@app.route('/assignment2')
def assignment2():
    return render_template('assignment2.html')

@app.route('/grades')
def grades():
    all_result = query_assignments()
    return render_template('grades.html', all_result=all_result)

@app.route('/studentgrades')
def studentgrades():
    if not session.get('name') or session.get('type') != 'student':
        return redirect(url_for('login'))

    acc = session['name']
    assignments = Assignments.query.filter_by(StuAcc=acc).all()

    return render_template('student_grades.html', assignments=assignments)


@app.route('/regrade', methods = ['POST', 'GET'])
def regrade():
    if request.method == 'GET':
        all_student = query_students()
        return render_template('regrade.html', all_student=all_student)
    else:
        all_student = query_students()
        id = request.form.get('id')
        name = request.form.get('name')
        mark = request.form.get('marks')
        if Assignments.query.filter_by(StuAcc=id, Name=name).first():
            flash('Student already has marks for that assignment. Please try a different one!', 'ERROR')
            return render_template('regrade.html', all_student=all_student)
        new = Assignments(Name=name, StuAcc=id, Marks=int(mark))
        db.session.add(new)
        db.session.commit()
        all_student = query_students()
        flash('Marks updated succesfully!')
        return render_template('regrade.html', all_student=all_student)

@app.route('/feedback')
def feedback():
    all_feedback = query_feedback()
    return render_template('feedback1.html', all_feedback=all_feedback)
    
@app.route('/labs')
def labs():
    return render_template('labs.html')
    
@app.route('/team')
def team():
    return render_template('team.html')
   
@app.route('/tests')
def tests():
    return render_template('tests.html')

@app.route('/remark', methods = ['GET', 'POST'])
def remark():
    if request.method == 'GET':
        all_remark = query_remarks()
        return render_template('remark.html', all_remark=all_remark)
    
    id = request.form.get('id')
    remarkview = db.session.query(Remarks, Assignments, Student).filter(Remarks.AID == Assignments.AID).filter(Assignments.StuAcc == Student.StuAcc).filter(Remarks.RID == int(id))[0]
    return render_template('remarkview.html', remarkview=remarkview)
    
@app.route('/remarkreq2', methods = ['POST'])
def remarkreq2():
    req = request.form.get('data')
    status, id = req.split('-')
    data = db.session.query(Remarks).filter(Remarks.RID == int(id))[0]
    data.Status = status
    db.session.commit()
    return req

@app.route('/remarkreq', methods = ['POST'])
def remarkreq():
    data = request.form.get('data')  
    import re
    match = re.match(r'^(Approved|Rejected)(\d+)$', data)
    if not match:
        return "Invalid request", 400

    status, rid = match.group(1), int(match.group(2))
    
    remark = Remarks.query.filter_by(RID=rid).first()
    if not remark:
        return "Remark not found", 404

    remark.Status = status
    db.session.commit()
    return data


@app.route('/submit_remark', methods=['POST'])
def submit_remark():
    if not session.get('name') or session.get('type') != 'student':
        return "Unauthorized", 403

    aid = request.form.get('aid')
    reason = request.form.get('reason')
    acc = session['name']
    print(aid)
    assignment = Assignments.query.get(aid)

    if not assignment:
        return "Unauthorized access to assignment", 403
    
    # # Prevent duplicate request
    # existing = Remarks.query.filter_by(AID=aid).first()
    # if existing:
        # return "Remark already submitted for this assignment.", 400

    remark = Remarks(AID=aid, Reason=reason, Status="Pending")
    db.session.add(remark)
    db.session.commit()  # ✅ DO NOT FORGET THIS
    return "Remark request submitted successfully!"


@app.route('/studentremark')
def studentremark():
    if not session.get('name') or session['type'] != 'student':
        return redirect(url_for('login'))

    acc = session['name']
    remarks = db.session.query(Remarks, Assignments, Student)\
        .join(Assignments, Remarks.AID == Assignments.AID)\
        .join(Student, Assignments.StuAcc == Student.StuAcc)\
        .filter(Student.StuAcc == acc)\
        .filter(Remarks.RID != None)\
        .all()

    print(f"📋 Found {len(remarks)} remarks for {acc}")
    for r, a, s in remarks:
        print(f"- RID: {r.RID}, Assignment: {a.Name}, Student: {s.StuAcc}, Status: {r.Status}")

    return render_template('student_remark.html', all_remark=remarks)


@app.route('/change', methods = ['POST'])
def change():
    id = request.form.get('id')
    marks = int(request.form.get('marks'))
    if marks > 100:
        marks = 100
    elif marks < 0:
        marks = 0
    data = db.session.query(Assignments).filter(Assignments.AID == int(id))[0]
    data.Marks = int(marks)
    db.session.commit()
    return [id, marks]
    
@app.route('/markview', methods = ['POST'])
def markview():
    id = request.form.get('id')
    data = db.session.query(Feedbacks).filter(Feedbacks.FID == int(id))[0]
    data.View = 1
    db.session.commit()
    return id

def query_students():
    all_student = db.session.query(Student)
    return all_student
    
def query_feedback():
    all_feedback = db.session.query(Feedbacks).filter(session.get("name") == Feedbacks.InsAcc)
    return all_feedback


@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'name' not in session or session.get('type') != 'student':
        return redirect(url_for('login'))

    instructors = Instructor.query.all()

    if request.method == 'POST':
        ins_acc = request.form['instructor']
        feedback_entries = [
            (1, request.form.get('q1')),
            (2, request.form.get('q2')),
            (3, request.form.get('q3')),
            (4, request.form.get('q4'))
        ]

        for qnum, content in feedback_entries:
            feedback = Feedbacks(
                InsAcc=ins_acc,
                Question=qnum,
                Title="Anonymous Feedback",
                content=content
            )
            db.session.add(feedback)

        db.session.commit()
        flash('Your feedback has been submitted successfully!')
        return redirect(url_for('submit_feedback'))

    return render_template('submit_feedback.html', instructors=instructors)




# def query_remarks():
#     all_remarks = db.session.query(Remarks, Assignments, Student).filter(Remarks.AID == Assignments.AID).filter(Assignments.StuAcc == Student.StuAcc)
#     return all_remarks

def query_remarks():
    return db.session.query(Remarks, Assignments, Student)\
        .join(Assignments, Remarks.AID == Assignments.AID)\
        .join(Student, Assignments.StuAcc == Student.StuAcc)\
        .all()




    
def query_assignments():
    all_assignments = db.session.query(Student, Assignments).filter(Student.StuAcc == Assignments.StuAcc)
    return all_assignments

if __name__ == '__main__':
    app.run(debug=True)