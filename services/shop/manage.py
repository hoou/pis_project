import coverage as coverage
import pytest
from flask.cli import FlaskGroup

from project import create_app, db

cov = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
cov.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    from project.store import user_store
    user_store.add(email='user1@server.eu', password='blah')
    user_store.add(email='user2@server.eu', password='blah-blah')

    from project.store import product_store
    product_store.add(name='Super product', price=19.99)
    product_store.add(name='Very bad product', price=2.99)


@cli.command()
def test():
    return pytest.main(['project/tests'])


@cli.command()
def coverage():
    result = pytest.main(['project/tests'])
    if result == 0:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        cov.html_report()
        cov.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
