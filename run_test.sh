dropdb -U postgres postgres_test
createdb -U postgres postgres_test
source test_setup.sh
python test.py