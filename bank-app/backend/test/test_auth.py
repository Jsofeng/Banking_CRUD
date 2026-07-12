from auth import hash_password, verify_password

def test_hash_password():
    password = "my_password123"

    hashed = hash_password(password)
    
    # The password should be hashed, Checks that the password was actually transformed if not assert would fail.
    assert hashed != password

    # Makes sure the function's return type is a str
    assert isinstance(hashed, str)


def test_verify_password():

    password = "my_secret_password"

    hashed_password = hash_password(password)

    result = verify_password(password, hashed_password)

    assert result == True

def test_verify_wrong_password():

    password = "my_secret_password"

    hashed_password = hash_password(password)

    result = verify_password("wrong_password", hashed_password)

    assert result == False