from sqlalchemy.orm import Session


class SqlalchemyRepository:
    def __init__(self, session: Session):
        self.session = session
