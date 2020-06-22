from flask import Flask, render_template, request, jsonify
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import sessionmaker, load_only
from pprint import pprint

app = Flask(__name__)

config = json.loads(open('config.json').read())
engine = create_engine(config['DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(INTEGER(11), primary_key=True)
    venue = Column(String(255), nullable=False)
    capacity = Column(String(255), nullable=False, server_default=text("'0'"))
    location = Column(String(255))
    state = Column(String(15))
    add_method = Column(String(50))


@app.route('/venue_api/v1', methods=['GET'])
def index():
    try:
        venue_query = request.args.get("venue")
        if venue_query:
            results = session.query(Venue).filter(Venue.venue.contains(venue_query)).all()
            venues = []
            for result in results:
                result = result.__dict__
                result['capacity'] = int(result['capacity'])
                del result['_sa_instance_state']
                del result['add_method']
                venues.append(result)

            if len(venues):
                return jsonify(venues)
            else:
                return jsonify([{"error": f"No venue found for following query: '{venue_query}'"}])

        else:
            return jsonify([{"error": f"No venue query requested."}])
    except (TypeError, KeyError, AttributeError) as e:
        return jsonify({"error": f"{e.__class__.__name__} - {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
