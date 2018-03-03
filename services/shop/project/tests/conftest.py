from project import create_app, db
import pytest


@pytest.fixture
def app():
    app_ = create_app()
    app_.config.from_object('project.config.TestingConfig')
    with app_.app_context():
        db.create_all()
        db.session.commit()
        yield app_
        db.session.remove()
        db.drop_all()


@pytest.fixture
def app_dev():
    app_ = create_app()
    app_.config.from_object('project.config.DevelopmentConfig')
    return app_


@pytest.fixture
def app_prod():
    app_ = create_app()
    app_.config.from_object('project.config.ProductionConfig')
    return app_


@pytest.fixture()
def db_session():
    yield db.session
