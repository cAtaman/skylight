from json import dumps, loads
from sms.config import db
from sms.src import utils
from sms.src.users import access_decorator
from sms.models.master import Master, MasterSchema, Props

all_fields = {'date_of_birth', 'email_address', 'grad_status', 'level', 'lga', 'mat_no', 'mode_of_entry', 'othernames',
              'phone_no', 'session_admitted', 'session_grad', 'sex', 'sponsor_email_address', 'sponsor_phone_no',
              'state_of_origin', 'surname'}
required = all_fields - {'grad_status', 'session_grad'}


@access_decorator
def get_exp(mat_no):
    # TODO remove 404 from exposed fns where check done in access decorator
    output = get(mat_no)
    if output:
        output.pop("is_symlink")
        output.pop("database")
        return dumps(output), 200
    return None, 404


@access_decorator
def post_exp(data):
    output = post(data)
    if output:
        return output, 400
    return None, 200


# ==============================================================================================
#                                  Core functions
# ==============================================================================================

def get(mat_no):
    db_name = utils.get_DB(mat_no)
    if not db_name:
        return None
    session = utils.load_session(db_name)
    student_data = session.PersonalInfo.query.filter_by(mat_no=mat_no).first()
    personal_info_obj = session.PersonalInfoSchema().dump(student_data)
    personal_info_obj['level'] = abs(personal_info_obj['level'])
    personal_info_obj.update({'grad_status': student_data.grad_status})
    return personal_info_obj


def post(data):
    data = data.copy()
    if utils.get_DB(data.get("mat_no")):
        return "Student already exists"
    if not all([data.get(prop) for prop in required]) or (data.keys() - all_fields):
        # Empty value supplied or Invalid field supplied or Missing field present
        return "Invalid field supplied or missing a compulsory field"
    if ("grad_status" not in data) or data.get("session_grad") == 0:
        # Check exceptions to non required
        return "Invalid field supplied or missing a compulsory field"

    session_admitted = data['session_admitted']

    master_schema = MasterSchema()
    database = "{}-{}.db".format(session_admitted, session_admitted + 1)
    master_model = master_schema.load({'mat_no': data['mat_no'], 'surname': data['surname'], 'database': database})

    session = utils.load_session(session_admitted)
    personalinfo_schema = session.PersonalInfoSchema()
    data["is_symlink"] = data["mode_of_entry"] - 1
    data["level"] = abs(data["level"]) * [1,-1][data.pop("grad_status")]
    student_model = personalinfo_schema.load(data)

    db.session.add(master_model)
    db.session.commit()

    db_session = personalinfo_schema.Meta.sqla_session

    if data["mode_of_entry"] != 1:
        # Point from Symlink table
        # TODO use util fn to predict class DB for DE students
        session_list = loads(Props.query.filter_by(key="SessionList").first().valuestr)
        class_session = session_list[session_list.index(session_admitted) - data["mode_of_entry"] + 1]
        student_model.database = "{}-{}.db".format(class_session, class_session + 1)
        symlink_session = utils.load_session(class_session)
        symlink_schema = symlink_session.SymLinkSchema()
        database = "{}-{}.db".format(session_admitted, session_admitted + 1)
        symlink_model = symlink_schema.load({"mat_no": data["mat_no"], "database": database})
        db_session_2 = symlink_schema.Meta.sqla_session
        db_session_2.add(symlink_model)
        db_session_2.commit()

    db_session.add(student_model)
    db_session.commit()


@access_decorator
def patch(data, superuser=False):
    data = data.copy()
    session = utils.get_DB(data.get("mat_no"))
    if not session:
        return None, 404
    if not all([data.get(prop) for prop in (required & data.keys())]) or (data.keys() - all_fields):
        # Empty value supplied or Invalid field supplied
        return "Invalid field supplied or missing a compulsory field", 400
    if data.get("session_grad") == 0:
        return "Invalid field supplied", 400

    session = utils.load_session(session)
    student = session.PersonalInfo.query.filter_by(mat_no=data["mat_no"])

    if superuser:
        level = abs(data.get("level",0)) or abs(student.first().level)
        if "grad_status" in data:
            data["level"] = level * [1,-1][data.pop("grad_status")]
        elif "level" in data:
            # Preserve grad status
            data["level"] = level * [1,-1][student.first().grad_status]
    else:
        for prop in ("session_admitted", "session_grad", "level", "mode_of_entry", "grad_status"):
            data.pop(prop, None)

    student.update(data)
    db_session = session.PersonalInfoSchema().Meta.sqla_session
    db_session.commit()
    return None, 200


@access_decorator
def delete(mat_no):
    session = utils.get_DB(mat_no)
    if not session:
        return None, 404
    session = utils.load_session(session)
    entries = []
    db_session = session.PersonalInfoSchema().Meta.sqla_session
    entries.append(session.PersonalInfo.query.filter_by(mat_no=mat_no).first())
    entries.append(session.GPA_Credits.query.filter_by(mat_no=mat_no).first())
    for lvl in range(100, 900, 100):
        entries.append(eval("session.CourseReg{}".format(lvl)).query.filter_by(mat_no=mat_no).first())
        entries.append(eval("session.Result{}".format(lvl)).query.filter_by(mat_no=mat_no).first())
    for entry in entries:
        if entry:
            db_session.delete(entry)
    master = Master.query.filter_by(mat_no=mat_no).first()
    db.session.delete(master)
    db_session.commit()
    db.session.commit()
    return None, 200
