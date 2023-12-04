"""init

Revision ID: 41c688d1ca3c
Revises: 
Create Date: 2023-12-04 13:05:41.745995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41c688d1ca3c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 't_dict_details', 't_dict_data', ['dict_data_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 't_hiker_rule', 't_hiker_developer', ['dev_id'], ['id'], ondelete='set null')
    op.create_foreign_key(None, 't_hiker_rule', 't_hiker_rule_type', ['type_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 't_perm_label_role', 't_roles', ['role_id'], ['id'])
    op.create_foreign_key(None, 't_perm_label_role', 't_perm_label', ['label_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 't_role_menu', 't_roles', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 't_role_menu', 't_menus', ['menu_id'], ['id'])
    op.create_foreign_key(None, 't_user_role', 't_users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 't_user_role', 't_roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 't_user_role', type_='foreignkey')
    op.drop_constraint(None, 't_user_role', type_='foreignkey')
    op.drop_constraint(None, 't_role_menu', type_='foreignkey')
    op.drop_constraint(None, 't_role_menu', type_='foreignkey')
    op.drop_constraint(None, 't_perm_label_role', type_='foreignkey')
    op.drop_constraint(None, 't_perm_label_role', type_='foreignkey')
    op.drop_constraint(None, 't_hiker_rule', type_='foreignkey')
    op.drop_constraint(None, 't_hiker_rule', type_='foreignkey')
    op.drop_constraint(None, 't_dict_details', type_='foreignkey')
    # ### end Alembic commands ###
