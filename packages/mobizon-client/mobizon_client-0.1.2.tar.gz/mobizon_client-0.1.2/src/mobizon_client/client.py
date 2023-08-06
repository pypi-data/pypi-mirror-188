from enum import Enum
import logging
import abc
from httpx import AsyncClient, Client
from mobizon_client import exceptions as exc
from mobizon_client.objects import Balance, MessageInfo, MessageStatus


class Service(str, Enum):
    GET_OWN_BALANCE = '/service/User/GetOwnBalance'
    LIST_MESSAGE = '/service/Message/List'
    SEND_SMS_MESSAGE = '/service/Message/SendSmsMessage'
    GET_MESSAGE_STATUS = '/service/Message/GetSMSStatus'


class AbstractMobizonClient(abc.ABC):
    _api = 'v1'
    _output = 'json'

    def __init__(self, url: str, api_key: str, logger: str = "mobizon-client"):
        self._url = url
        self._api_key = api_key
        self._logger = logging.getLogger(logger)
        self._init()

    @abc.abstractmethod
    def _init(self):
        raise NotImplementedError()

    @staticmethod
    def _normalize_response(response):
        if not response.is_success:
            raise exc.UnknownError()

        result = response.json()

        if result.get('code', None) != 0:
            raise exc.RequestError(
                code=response.get('code', 999),
                message=response.get('message', 'Request error'),
            )

        return result.get('data')

    @abc.abstractmethod
    def request(self, service: Service, params: dict = None, payload: dict = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_message(self, recipient: str, text: str, sender_signature: str = None) -> MessageInfo:
        """
        Отправка одиночного SMS сообщения
        :param recipient: Получатель SMS сообщения - номер в международном формате, если в номере есть + в начале, то его следует закодировать в URL сущность %2B или удалить, оставив только цифры.
        :param text: Текст SMS сообщения, закодированный в URL сущность.
        :param sender_signature: Подпись отправителя. Можно не указывать, тогда в случае, если нет ни одной валидной подписи, будет использована общая системная подпись.
        :return: MessageInfo
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_message_status(self, ids: list[str]) -> list[MessageStatus]:
        """
        Получение отчета о статусе доставки SMS сообщения
        :param ids:	Идентификатор(ы) сообщения - массив или строка идентификаторов, разделенных запятыми. Максимум 100 штук.
        :return: MessageStatus
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_balance(self) -> Balance:
        """
        Получение информации о балансе
        :return: Balance
        """
        raise NotImplementedError()


class AsyncMobizonClient(AbstractMobizonClient):
    _client: AsyncClient

    async def request(self, service: Service, params: dict = None, payload: dict = None):
        response = await self._client.post(url=service, params=params, json=payload)
        return self._normalize_response(response)

    def _init(self):
        self._client = AsyncClient(base_url=self._url, params=dict(
            output=self._output,
            api=self._api,
            apiKey=self._api_key,
        ))

    async def close(self):
        await self._client.aclose()

    async def send_message(self, recipient: str, text: str, sender_signature: str = None) -> MessageInfo:
        payload = {
            "recipient": recipient,
            "text": text,
            "from": sender_signature,
        }
        response = await self.request(service=Service.SEND_SMS_MESSAGE, payload=payload)
        return MessageInfo.restore(response)

    async def get_message_status(self, ids: list[str]) -> list[MessageStatus]:
        payload = {"ids": ids}
        response = await self.request(service=Service.GET_MESSAGE_STATUS, payload=payload)
        return list(map(MessageStatus.restore, response))

    async def get_balance(self) -> Balance:
        response = await self.request(service=Service.GET_OWN_BALANCE)
        return Balance.restore(response)


class MobizonClient(AbstractMobizonClient):
    _client: Client

    def request(self, service: Service, params: dict = None, payload: dict = None):
        response = self._client.post(url=service, params=params, json=payload)
        return self._normalize_response(response)

    def _init(self):
        self._client = Client(base_url=self._url, params=dict(
            output=self._output,
            api=self._api,
            apiKey=self._api_key,
        ))

    def close(self):
        self._client.close()

    def send_message(self, recipient: str, text: str, sender_signature: str = None) -> MessageInfo:
        payload = {
            "recipient": recipient,
            "text": text,
            "from": sender_signature,
        }
        response = self.request(service=Service.SEND_SMS_MESSAGE, payload=payload)
        return MessageInfo.restore(response)

    def get_message_status(self, ids: list[str]) -> list[MessageStatus]:
        payload = {"ids": ids}
        response = self.request(service=Service.GET_MESSAGE_STATUS, payload=payload)
        return list(map(MessageStatus.restore, response))

    def get_balance(self) -> Balance:
        response = self.request(service=Service.GET_OWN_BALANCE)
        return Balance.restore(response)
