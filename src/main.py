"""Module main.py"""
import logging
import os
import sys

import boto3


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info(arguments)

    # Setting up
    src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

    # Steps
    data = src.data.interface.Interface(
        s3_parameters=s3_parameters, arguments=arguments).exc()
    data.info()

    '''
    Cache
    '''
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.data.interface
    import src.functions.cache
    import src.functions.service
    import src.s3.configurations
    import src.s3.s3_parameters
    import src.setup

    # Amazon: Connector, S3 Parameters, Service
    connector = boto3.session.Session()
    s3_parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
    service = src.functions.service.Service(connector=connector, region_name=s3_parameters.region_name).exc()

    # Modelling arguments
    arguments = src.s3.configurations.Configurations(connector=connector).objects(
        key_name=('architecture' + '/' + 'single' + '/' + 'parts' + '/' + 'arguments.json'))

    main()
