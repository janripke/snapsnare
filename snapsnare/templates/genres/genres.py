from datetime import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required

from snapsnare.repositories.genre.genre_repository import GenreRepository
from snapsnare.repositories.section.section_repository import SectionRepository
genres = Blueprint('genres', __name__, template_folder='templates')


@genres.route('/genres', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        connector = current_app.connector
        genre_repository = GenreRepository(connector)
        section_repository = SectionRepository(connector)
        genres_ = genre_repository.list_by(active=1, order_by='genre')
        sections = section_repository.list()
        connector.close()

        return render_template('genres/genres.html', genres=genres_, sections=sections)
