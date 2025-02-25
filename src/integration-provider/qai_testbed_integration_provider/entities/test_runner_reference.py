# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class TestRunnerReferenceMapper(sql_db.Model):

    __tablename__ = 'M_TestRunnerReference'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    reference = sa.Column(sa.String, nullable=False)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))
