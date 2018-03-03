from flask.cli import FlaskGroup

from project import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    from project.api.models import User
    db.session.add(User('user1@server.eu', 'blah'))
    db.session.add(User('user2@server.eu', 'blah-blah'))
    db.session.commit()


@cli.command()
def test():
    import pytest
    return pytest.main(['project/tests'])


if __name__ == '__main__':
    cli()
