from flask import Blueprint, render_template
from flask_login import login_required

from simpledu.models import Course, Chapter

course = Blueprint('course', __name__, url_prefix='/courses')


@course.route("/<int:id>")
@login_required
def detail(id):
    course = Course.query.get_or_404(id)
    return render_template('detail.html', course=course)


@course.route('/<int:course_id>/chapters/<int:chapter_id>/')
@login_required
def chapter(course_id, chapter_id):
    chapter = Chapter.query.get(chapter_id)
    return render_template('chapter.html', chapter=chapter)
