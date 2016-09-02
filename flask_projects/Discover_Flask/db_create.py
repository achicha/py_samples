from project import db
from project.models import BlogPost

# create the database and the db tables via SQLAlchemy
db.create_all()

# insert some data
db.session.add(BlogPost("Good", "I\'m good.", 1))
db.session.add(BlogPost("Well", "I\'m well.", 1))

# commit the changes
db.session.commit()
