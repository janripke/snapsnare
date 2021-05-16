from flask import Blueprint, render_template
from flask import request
from snapsnare.templates.components import jammers
from snapsnare.templates.components import activities
from snapsnare.templates.components import sections
from snapsnare.templates.components import section
from snapsnare.templates.components import code


index = Blueprint('index', __name__, template_folder='templates')


@index.route('/')
def show():
    if request.method == 'GET':

        return render_template(
            'index/index.html',
            sections=sections.load(),
            code=code.load(),
            activities=activities.load(),
            section=section.load(),
            jammers=jammers.load(),
        )
