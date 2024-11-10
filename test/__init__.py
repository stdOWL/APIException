import unittest
from api_exception.exception import APIException
from custom_enum.enums import ExceptionCode, ExceptionStatus
from schemas.response_model import ResponseModel


class TestAPIException(unittest.TestCase):

    def test_api_exception(self):
        # Test creating an APIException instance
        exception = APIException(error_code=ExceptionCode.AUTH_LOGIN_FAILED)
        self.assertEqual(exception.error_code, "AUTH-1000")
        self.assertEqual(exception.message, "Incorrect username and password.")
        self.assertEqual(exception.description, "Failed authentication attempt.")
        self.assertEqual(exception.status, ExceptionStatus.FAIL)
        self.assertEqual(exception.http_status_code, 400)

        # Test the response dictionary
        response = exception.to_response()
        expected_response = {
            "error_code": "AUTH-1000",
            "status": "FAIL",
            "message": "Incorrect username and password.",
            "description": "Failed authentication attempt."
        }
        self.assertEqual(response, expected_response)

    def test_response_model(self):
        # Test creating a ResponseModel instance for success response
        response = ResponseModel(data={"key": "value"})
        self.assertEqual(response.status, ExceptionStatus.SUCCESS)
        self.assertEqual(response.message, "Operation completed successfully.")
        self.assertIsNone(response.error_code)
        self.assertIsNone(response.description)
        self.assertEqual(response.data, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
