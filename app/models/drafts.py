from app.extensions import db


class Draft(db.Model):
    __bind_key__ = 'drafts'
    __tablename__ = 'drafts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer)
