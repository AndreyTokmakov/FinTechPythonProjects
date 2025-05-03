import configparser
import os
from dataclasses import dataclass

project_dir: str = os.path.dirname(os.path.realpath(__file__))
file_path: str = f'{project_dir}/../private_credentials.conf'


@dataclass
class Credentials(object):
    api_key: str = ""
    api_secret: str = ""
    private_key_path: str = ""


def get_configuration_section(name: str) -> configparser.SectionProxy:
    config = configparser.ConfigParser()
    config.read(file_path)
    return config[name]


class GateIoConfiguration:

    @staticmethod
    def read_credentials() -> Credentials:
        data: configparser.SectionProxy = get_configuration_section('gate.io')
        return Credentials(api_key=data['api_key'], api_secret=data['api_secret'])

    @staticmethod
    def read_credentials_testnet() -> Credentials:
        data: configparser.SectionProxy = get_configuration_section('gate.io.testnet-2')
        return Credentials(api_key=data['api_key'], api_secret=data['api_secret'])


class ByBitConfiguration:

    @staticmethod
    def read_credentials() -> Credentials:
        data: configparser.SectionProxy = get_configuration_section('by.bit')
        return Credentials(api_key=data['api_key'], api_secret=data['api_secret'])


class BinanceConfiguration:

    @staticmethod
    def read_credentials() -> Credentials:
        data: configparser.SectionProxy = get_configuration_section('binance')
        return Credentials(api_key=data['api_key'], private_key_path=data['private_key_path'])
