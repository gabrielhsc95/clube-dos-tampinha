from cassandra.cluster import Session

from const import KEY_SPACE


def create_teacher(session: Session, user_id: str):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.teacher 
                (user_id  , students)
            VALUES 
                ({user_id}, null);
        """
    )
