from cassandra.cluster import Session

from const import KEY_SPACE


def create_parent(session: Session, user_id: str):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.parent 
                (user_id  , children, payments)
            VALUES 
                ({user_id}, null    , null);
        """
    )
