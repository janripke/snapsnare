from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_required


from snapsnare.system import dictionaries
from snapsnare.repositories.genre.genre_repository import GenreRepository
from snapsnare.repositories.section.section_repository import SectionRepository

genre = Blueprint('genre', __name__, template_folder='templates')


@genre.route('/genre', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    genre_repository = GenreRepository(connector)
    section_repository = SectionRepository(connector)

    sections = section_repository.list()

    role = session.get('role', 'user')
    if role != 'admin':
        return redirect(url_for('login.show'))

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')

        if uuid_:
            genre_ = genre_repository.find_by_uuid(uuid_)
            genre_ = dictionaries.strip_none(genre_)

            connector.close()
            return render_template('genre/genre.html', sections=sections, genre=genre_)

        genre_ = {
        }

        return render_template('genre/genre.html', sections=sections, genre=genre_)

    if request.method == 'POST':
        uuid_ = request.form['uuid']
        name = request.form['genre']

        if uuid_:
            genre_ = {
                'uuid': uuid_,
                'genre': name
            }
            genre_repository.update(genre_)

            connector.commit()
            connector.close()
            flash('De genre details zijn bijgewerkt.', 'info')
            return redirect(url_for('genres.show'))

        genre_ = {
            'genre': name
        }

        genre_repository.insert(genre_)
        connector.commit()
        connector.close()
        flash('Het genre is toegevoegd.', 'info')
        return redirect(url_for('genres.show'))
