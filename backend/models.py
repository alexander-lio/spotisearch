from config import db

class Contact(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    track = db.Column(db.String(80), unique=False, nullable=False)
   
    def to_json(self) :
        return {
            "id": self.id,
            "track": self.track,
        }