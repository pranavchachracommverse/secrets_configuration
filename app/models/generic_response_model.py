from pydantic import BaseModel
from typing import Union, Optional


class GenericApiResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    data: Optional[Union[dict, list, str]] = None

    @classmethod
    def success_response(cls,
                         data: Optional[Union[dict, list, str]] = None
                         ):
        """
        Factory method to create a success response.
        :param data: Optional data to include in the response.
        :return: GenericApiResponse instance with success=True.
        """
        return cls(success=True, data=data)

    @classmethod
    def failure_response(cls,
                         error: Union[str, list[str]]
                         ) -> 'GenericApiResponse':
        """
        Factory method to create a failure response.
        :param error: Error message to include in the response.
        :return: GenericApiResponse instance with success=False.
        """
        if not isinstance(error, (str, list)):
            raise TypeError("The 'error' parameter must be of type 'str' or 'list[str]'.")

        if isinstance(error, list) and all(isinstance(item, str) for item in error):
            error = ' | '.join(error)

        return cls(success=False, error=error)