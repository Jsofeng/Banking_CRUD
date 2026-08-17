from unittest.mock import MagicMock, patch

from main import get_db


def test_get_db_yields_session_and_closes():

    mock_db = MagicMock()  # creates a fake database connection

    with patch(
        "main.SessionLocal", return_value=mock_db
    ):  # temporarily changes SessionLocal
        """
        before:
            get_db()
            |
            v
            SessionLocal()
            |
            v
            Real database session

        after patch:
            get_db()
            |
            v
            SessionLocal()
            |
            v
            mock_db
        """

        db_generator = get_db()

        # Run until yield
        db = next(db_generator)

        # Check it returns the session
        assert db == mock_db

        # Finish generator to trigger finally block
        try:
            next(db_generator)
        except StopIteration:
            pass

        # Did the database session get closed exactly once?
        mock_db.close.assert_called_once()
