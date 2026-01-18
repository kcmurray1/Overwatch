from app.models import Machine, Watchlist, Project
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MachineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Machine

        # allow creation of Model
        load_instance = True


class WatchlistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Watchlist
        load_instance = True

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        include_fk = True