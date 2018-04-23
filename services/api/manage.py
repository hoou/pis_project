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
    admin = users.add(User(email='tibor@mikita.eu', password='admin123'))
    admin.active = True
    admin.role = UserRole.ADMIN

    user = users.add(User(email='peter@hnat.eu', password='user123'))
    user.active = True
    user.role = UserRole.CUSTOMER

    worker = users.add(User(email='samuel@jaklovsky.eu', password='worker123'))
    worker.active = True
    worker.role = UserRole.WORKER

    from project.business import categories
    category_tractors = categories.add(Category('Tractors'))
    category_trailers = categories.add(Category('Trailers'))

    categories.add_product(category_tractors, Product(name='Zetor', price=180000))
    categories.add_product(category_tractors, Product(name='New Holland', price=130000))
    categories.add_product(category_tractors, Product(name='John Deere', price=150000))
    categories.add_product(category_trailers, Product(name='Marshall 14T', price=7000))
    categories.add_product(category_trailers, Product(name='Bailey 16T', price=8000))


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
