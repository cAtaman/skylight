from json import dumps
from sms.config import db
from sms.src.users import access_decorator
from sms.models.courses import Courses, CoursesSchema, Options

# TODO Create endpoint for teaching departments
# TODO Change primary key of all courses models from it's course_code to an id
#      As it stands, a course's code can't be modified


def get(course_code):
    course = Courses.query.filter_by(course_code=course_code).first()
    return CoursesSchema().dump(course)


def get_course_details(course_code=None, level=None, options=False, inactive=False):
    if course_code:
        output = [get(course_code)]
    else:
        output = get_all(level, options, inactive)
    if output:
        return output, 200
    return None, 404


def get_all(level=None, options=False, inactive=False):
    courses = Courses.query
    if level:
        courses = courses.filter_by(course_level=level)
    if not inactive:
        courses = courses.filter_by(active=1)
    if options:
        course_list = courses.all()
    else:
        course_list = courses.filter_by(options=0).all()
        for option in Options.query.all():
            option_member = courses.filter_by(options=option.options_group).first()
            if option_member:
                course_list += [option_member]
    return CoursesSchema(many=True).dump(course_list)


@access_decorator
def post(course):
    course_obj = Courses(**course)
    db.session.add(course_obj)
    db.session.commit()


@access_decorator
def put(data):
    error_log = []
    for course in data:
        course_level = course['course_level']
        exec('from sms.models.courses import Courses{} as Courses'.format(course_level))
        course_obj = eval('Courses').query.filter_by(course_code=course['course_code']).first()
        if not course_obj:
            msg = course['course_code'] + ' not found'
            error_log.append(msg)
            continue
        for k, v in course.items():
            setattr(course_obj, k, v)
        db.session.add(course_obj)
    db.session.commit()
    return error_log, 200


@access_decorator
def delete(course_code):
    course_obj = Courses.query.filter_by(course_code=course_code).first()
    if not course_obj:
        return None, 404
    db.session.delete(course_obj)
    db.session.commit()