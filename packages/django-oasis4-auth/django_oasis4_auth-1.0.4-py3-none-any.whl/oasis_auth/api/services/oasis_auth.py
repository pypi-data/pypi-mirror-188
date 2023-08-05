# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2022. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2022. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         20/12/22 12:13 PM
# Project:      CFHL Transactional Backend
# Module Name:  oasis_auth
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError as CoreValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from oasis.models import Client
from oasis_auth.lib.utils import AuthActions
from oasis_auth.lib.utils import SendCode
from rest_framework import status
from rest_framework.response import Response
from uuid import uuid4
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.exceptions import AuthenticationFailed
from zibanu.django.rest_framework.exceptions import ValidationError
from zibanu.django.rest_framework.viewsets import ViewSet
from zibanu.django.utils import CodeGenerator
from zibanu.django.utils import ErrorMessages

from oasis.tasks import sync_company


class OasisAuthServices(ViewSet):
    """
    Set of POST endpoints for REST services.
    """
    __cache_timeout = settings.OASIS_AUTH_CODE_TIMEOUT
    __cache_timeout_seconds = __cache_timeout * 60
    __user = get_user_model()

    def register(self, request) -> Response:
        """
        REST service to get data and send code for register process.
        :param request: request data from HTTP
        :return: response object
        """
        try:
            if {"customer_id", "email", "password"} <= request.data.keys():
                user = self.__user.objects.filter(email__exact=request.data.get("email"))
                if user.count() == 0:
                    customer = Client.objects.get_customer(request.data.get("customer_id"), request.data.get("email"))
                    if customer.is_valid:
                        code_generator = CodeGenerator("register")
                        data_cache = code_generator.generate_dict()
                        data_cache["password"] = request.data.get("password")
                        cache_key = data_cache.pop("uuid").hex
                        customer_data = {
                            "first_name": customer.first_name,
                            "last_name": customer.last_name,
                            "location": customer.location,
                            "address": customer.address,
                            "phone": customer.phone,
                            "mobile": customer.celphone,
                            "email": customer.email,
                            "customer_id": customer.clientid,
                            "document_type": customer.clienttype,
                            "is_valid": customer.is_valid,
                            "type": customer.customer_type,
                        }
                        data_return = {
                            "token": cache_key,
                            "data": customer_data
                        }
                        # Set data cache to store in
                        data_cache["data"] = customer_data
                        # Send Mail
                        email_context = {
                            "customer_name": customer.clientname,
                            "customer_code": data_cache.get("code"),
                            "code_timeout": settings.OASIS_AUTH_CODE_TIMEOUT,
                            "email_datetime": timezone.now().astimezone(tz=timezone.get_default_timezone()).strftime(
                                "%Y-%m-%d %H:%M:%S"),
                            "email_id": str(uuid4())
                        }
                        # Send code mail
                        send_code = SendCode(to=customer_data.get("email"), action=data_cache.get("action"),
                                             context=email_context)
                        if send_code.load_templates():
                            send_code.send()
                        # Store data_cache in cache
                        cache.set(cache_key, data_cache, self.__cache_timeout_seconds)
                        status_return = status.HTTP_200_OK
                    else:
                        raise APIException(
                            msg=_("The client id or email is invalid. Please confirm your details at the "
                                  "nearest office and try again."), error=_("Invalid data"),
                            http_status=status.HTTP_412_PRECONDITION_FAILED)
                else:
                    raise ValidationError(_("The user is previously registered."))
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
        except CoreValidationError as exc:
            raise APIException(msg=exc.message, error=_("Error at database validations"),
                               http_status=status.HTTP_412_PRECONDITION_FAILED) from exc
        except APIException as exc:
            raise APIException(msg=exc.detail.get("message"), error=exc.detail.get("error"),
                               http_status=exc.status_code) from exc
        except self.__user.DoesNotExist as exc:
            raise APIException(msg=_("Customer does not exist."), http_status=status.HTTP_400_BAD_REQUEST) from exc
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error="register", http_status=exc.status_code) from exc
        except Exception as exc:
            raise APIException(msg=_("Not controlled exception error."), error=str(exc)) from exc
        else:
            return Response(status=status_return, data=data_return)

    def validate_code(self, request) -> Response:
        """
        Method to validate authentication code with token.
        :param request: request data from HTTP
        :return: response object widht http status code
        """
        try:
            if request.data and {"token", "code"} <= request.data.keys():
                cache_key = request.data.get("token")
                # Get DataCache
                data_cache = cache.get(cache_key)
                if data_cache:
                    if request.data.get("code") == data_cache.get("code"):
                        # Make actions using class AuthAction.
                        auth_action = AuthActions(data_cache)
                        data_result = auth_action.do_action()
                        status_return = status.HTTP_200_OK
                    else:
                        raise ValidationError(_("The code does not match."))
                else:
                    raise ValidationError(_("The code has expired. Please request a new authorization code."))
            else:
                raise APIException(ErrorMessages.DATA_REQUEST_NOT_FOUND, "validate_code",
                                   status.HTTP_406_NOT_ACCEPTABLE)
        except ValidationError as exc:
            raise APIException(str(exc)) from exc
        except CoreValidationError as exc:
            raise APIException(msg=exc.message, error="validate_code",
                               http_status=status.HTTP_412_PRECONDITION_FAILED) from exc
        except APIException as exc:
            raise APIException(exc.detail.get("message"), exc.detail.get("detail"), exc.status_code) from exc
        except Exception as exc:
            raise APIException(str(exc)) from exc
        else:
            return Response(status=status_return, data=data_result)

    def login(self, request) -> Response:
        """
        Method to expose authentication REST Service.
        :param request: request data from HTTP
        :return: response object
        """
        try:
            if request.data:
                if {"email", "password"} <= request.data.keys():
                    username = self.__user.objects.get(email__exact=request.data.get("email")).username
                    user = authenticate(username=username, password=request.data.get("password"))
                    if user is not None:
                        code_generator = CodeGenerator("login")
                        data_cache = code_generator.generate_dict()
                        cache_key = data_cache.pop("uuid").hex
                        data_cache["data"] = user
                        data_return = {
                            "token": cache_key
                        }
                        email_context = {
                            "customer_name": user.get_full_name(),
                            "customer_code": data_cache.get("code"),
                            "code_timeout": self.__cache_timeout_seconds,
                            "email_datetime": timezone.now().astimezone(tz=timezone.get_default_timezone()).strftime(
                                "%Y-%m-%d %H:%M:%S"),
                            "email_id": str(uuid4())
                        }
                        # Send a second pass authentication code
                        send_code = SendCode(to=request.data.get("email"), action=data_cache.get("action"),
                                             context=email_context)
                        if send_code.load_templates():
                            send_code.send()
                        # Store data in cache
                        cache.set(cache_key, data_cache, self.__cache_timeout_seconds)
                        status_return = status.HTTP_200_OK
                    else:
                        raise AuthenticationFailed(_("Email or Password incorrect."))
                else:
                    raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error="login", http_status=exc.status_code) from exc
        except self.__user.DoesNotExist:
            raise AuthenticationFailed(_("Email or Password incorrect."))
        else:
            return Response(status=status_return, data=data_return)
