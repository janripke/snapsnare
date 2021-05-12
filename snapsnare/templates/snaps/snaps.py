from flask import Blueprint, render_template
from flask import request
from flask_login import login_required

from snapsnare.templates.components import jammers
from snapsnare.templates.components import sections
from snapsnare.templates.components import section
from snapsnare.templates.components import code
from snapsnare.templates.components import samples
from snapsnare.templates.components import activities
from snapsnare.templates.components import my_samples
snaps = Blueprint('snaps', __name__, template_folder='templates')


@snaps.route('/snaps')
@login_required
def show():
    if request.method == 'GET':

        return render_template(
            'snaps/snaps.html',
            sections=sections.load(),
            code=code.load(),
            snaps=samples.load(),
            my_snaps=my_samples.load(),
            section=section.load(),
            jammers=jammers.load(),
            activities=activities.load()
        )
