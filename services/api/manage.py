import coverage as coverage
import pytest
from flask.cli import FlaskGroup

from project import create_app, db
from project.models.category import Category
from project.models.product import Product
from project.models.user import User, UserRole

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
    from project.business import users
    user = users.add(User(email='tibor@mikita.eu', password='admin123'))
    user.active = True
    user.role = UserRole.ADMIN

    from project.business import categories
    category = categories.add(Category('Men'))

    categories.add_product(category, Product(name='Super product', price=19.99))
    categories.add_product(category, Product(name='Very bad product', price=2.99))


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
