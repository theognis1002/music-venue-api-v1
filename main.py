import json

from flask import Flask, jsonify, render_template, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app=app, version='1.0', default='Endpoints', default_label='GET/POST venue information', title='Music & Sports Venue API', prefix='/api/v1')
ns = api.namespace('Venues', description='')

config = json.loads(open('config.json').read())
engine = create_engine(config['DATABASE_URI'])
db = SQLAlchemy(app)

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


my_fields = api.model('MyModel', {
    'name': fields.String
})


@api.route('/', methods=['GET'])
@api.doc(False)
class VenueEndpoints(Resource):
    def get(self):
        """list route endpoints"""
        endpoints = []

        for r in app.url_map._rules:
            if r.rule == '/static/<path:filename>':
                continue

            route = {"route": r.rule,
                    "description": r.endpoint.replace("_", " "),
                    "methods": [method for method in list(r.methods) 
                                if method != 'HEAD' and method != 'OPTIONS']}
            endpoints.append(route)

        return render_template('index.html', endpoints=endpoints, request=request)


@ns.param('venue', 'Search database by venue name or substring')
@api.route('/venues', methods=['GET', 'POST'])
class VenueInfo(Resource):
    def get(self):
        """get venue information from database"""
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
                    response = jsonify(venues)
                    response.status_code = 200
                    return response
                else:
                    response = jsonify([{"error": f"No venue found for following query: '{venue_query}'"}])
                    response.status_code = 404
                    return response

            else:
                venues = session.query(Venue).all()
                response = jsonify(venues)
                response.status_code = 200
                return response

        except (TypeError, KeyError, AttributeError) as e:
            response = jsonify({"error": f"{e.__class__.__name__} - {str(e)}"})
            response.status_code = 400
            return response

    @ns.param('venue', 'Search database by venue name or substring')
    @ns.param('capacity', 'Maximum venue capacity', type='Integer')
    @ns.param('location', 'City name')
    @ns.param('state', 'State abbreviation (ie; CA)')
    def post(self):
        """add venue information to database"""
        if request.method == 'POST':
            print(request.args)
            required_args = ['venue', 'capacity', 'location', 'state']

            if all(args in request.args for args in required_args):

                try:
                    new_venue = Venue(request.args.to_dict())
                    session.add(new_venue)
                    session.commit()
                    response = jsonify({"result": "success"})
                    response.status_code = 200
                    return response

                except (TypeError, KeyError) as e:
                    response = jsonify({"error": str(e)})
                    response.status_code = 400
                    return response

            else:
                response = jsonify({"error": "missing arg(s)"})
                response.status_code = 400
                return response


@ns.param('venue', 'Search database by venue name or substring')
@api.route('/venues/<int:venue_id>', methods=['GET', 'POST'])
class VenueDetailsInfo(Resource):
    def get(self, venue_id):
        """get venue information from database"""
        try:

            venue = session.query(Venue).get(venue_id)
            response = jsonify(venue)
            response.status_code = 200
            return response

        except Exception as e:
            response = jsonify({"error": f"{e.__class__.__name__} - {str(e)}"})
            response.status_code = 400
            return response

if __name__ == '__main__':
    app.run(debug=True)

