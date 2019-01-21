from expenses import db
from expenses.models import Expense


db.create_all()
# user = User(name='leustad', password='$2b$12$d/ECye.LlGnA/JEBJ2ejiOi2i81nI7gufBOsQB7hCD9Hk9YIRy/sG', role='admin', active=None)
# db.session.add(user)
db.session.commit()
