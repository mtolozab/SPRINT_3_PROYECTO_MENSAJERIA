from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_file
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint('inbox', __name__, url_prefix='/inbox')

@bp.route("/getDB")
@login_required
def getDB():
    return send_file(current_app.config['DATABASE'], as_attachment=True)


@bp.route('/show')
@login_required
def show():
    db = get_db() #SE CAMBIO =
    messages = db.execute(
        'SELECT u.username AS username, m.subject AS subject, m.body AS body, m.created AS created'
        ' FROM (select * from message where to_id=' + str(g.user['id']) + ') AS m JOIN User u ON  m.from_id = u.id'
        ' ORDER BY created DESC' # CAMBIADO EL QUERY VIERNES
    ).fetchall()

    return render_template('/inbox/show.html', messages=messages) #SE CAMBIO VIERNES


@bp.route('/send', methods=('GET', 'POST'))
@login_required
def send():
    if request.method == 'POST':        
        from_id = g.user['id']
        to_username = request.form['to']        #SE CAMBIO VIERNES=
        subject = request.form['subject']        #SE CAMBIO =
        body = request.form['body']        #SE CAMBIO =

        db = get_db() #SE CAMBIO =
       
        if not to_username:
            flash('To field is required')
            return render_template('inbox/send.html')    #SE CAMBIO TEM
        
        if not subject:       #SE CAMBIO ANTES DE LOS 2PUNTOS
            flash('Subject field is required')
            return render_template('inbox/send.html')
        
        if not body:           #SE CAMBIO ANTES DE LOS 2PUNTOS
            flash('Body field is required')
            return render_template('inbox/send.html')    #SE CAMBIO TEM
        
        error = None    
        userto = None 
        
        userto = db.execute(
            'SELECT * FROM user WHERE username = ?', (to_username,)  # SE CAMBIO QUERY  VIERNES
        ).fetchone()
        
        if userto is None:
            error = 'Recipient does not exist'
     
        if error is not None:
            flash(error)
        else:
            db = get_db() #SE CAMBIO =
            db.execute(
                'INSERT INTO message (from_id, to_id, subject, body)' # se cambió query el viernes
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], userto['id'], subject, body)
            )
            db.commit()

            return redirect(url_for('inbox.show'))

    return render_template('inbox/send.html')