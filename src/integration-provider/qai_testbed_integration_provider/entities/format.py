# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db
from sqlalchemy.orm import relationship


class FormatMapper(sql_db.Model):

    __tablename__ = 'M_Format'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    format_ = sa.Column(sa.String, unique=True)
    mime_type = sa.Column(sa.String)

    resource_type_id = sa.Column(sa.Integer, sa.ForeignKey('M_ResourceType.id'))

    resource_type = relationship('ResourceTypeMapper')

