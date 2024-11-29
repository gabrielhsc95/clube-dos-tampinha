from cassandra.cluster import Session

from const import KEY_SPACE


def create_student(session: Session, user_id: str):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.student 
                (user_id  , parents, activities)
            VALUES 
                ({user_id}, null   , null);
        """
    )
