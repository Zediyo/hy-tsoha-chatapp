from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy(app)

def create_tables_if_missing():
	result = db.session.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'admins');"))

	if result.fetchone()[0] == False:
		schema_file = "schema.sql"
		with open(schema_file, "r") as file:
			schema_sql = file.read()
			print("Creating tables...")
			db.session.execute(text(schema_sql))
			db.session.commit()


def drop_all_tables():
	result = db.session.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'admins');"))
	
	if result.fetchone()[0] == True:
		print("Dropping tables...")
		db.session.execute(text("""
			DO $$
			DECLARE
			row record;
			BEGIN
				FOR row IN SELECT * FROM pg_tables WHERE schemaname = 'public' 
				LOOP
				EXECUTE 'DROP TABLE public.' || quote_ident(row.tablename) || ' CASCADE';
				END LOOP;
			END;
			$$;
		"""))
		db.session.commit()

with app.app_context():
	# drop_all_tables()
	create_tables_if_missing()