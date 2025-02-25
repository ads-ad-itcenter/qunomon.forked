# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.file_system import GetFileSystemsResSchema
from ...usecases.file_system import FileSystemService
from ...across.exception import QAIException


logger = get_logger()


class FileSystemAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = FileSystemService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_file_system()
            return GetFileSystemsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='I99999', message='internal server error: {}'.format(e))), 500
