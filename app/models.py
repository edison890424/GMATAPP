from app import db

class StudentDatabase(db.Model):
    __tablename__ = '学生数据库'
    student_id = db.Column('学员编号', db.String, primary_key=True)
    name = db.Column('姓名', db.String, nullable=False)
    registration_time = db.Column('报名时间', db.String, nullable=True)
    class_number = db.Column('班号', db.String, nullable=True)
    verification_number = db.Column('验证号', db.String, nullable=True)
    gender = db.Column('性别', db.String, nullable=True)
    mock_exam_score = db.Column('模考分', db.Integer, nullable=True)
    target_score = db.Column('目标分', db.Integer, nullable=True)
    exam_score = db.Column('考试分', db.Integer, nullable=True)
    attended_classes = db.Column('参加过的班级', db.String, nullable=True)
    education_work_background = db.Column('教育_工作背景', db.String, nullable=True)
    qq = db.Column('QQ', db.String, nullable=True)
    email = db.Column('邮箱', db.String, nullable=True)
    phone = db.Column('电话', db.String, nullable=True)
    trial_period_verification_code = db.Column('试用期验证码', db.String, nullable=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
