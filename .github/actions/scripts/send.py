import pika
import sys
import yaml
import json


def parse_domain_yaml(domain_file: str) -> dict:
    with open(domain_file, 'r') as f:
        content = yaml.safe_load(f)
    return content

def parse_data_product_yaml(data_product_file: str) -> dict:
    with open(data_product_file, 'r') as f:
        content = yaml.safe_load(f)
    return content

def send(message_body: dict) -> None:
    connection = pika.BlockingConnection(pika.URLParameters('amqp://admin:admin@rabbitmq:5672/'))
    channel = connection.channel()
    channel.queue_declare('DomainGitops')

    channel.basic_publish(exchange='DataMesh', routing_key='domain.HasChanges', body=json.dumps(message_body))

    connection.close()

if __name__ == "__main__":
    changed_files = sys.argv[1]
    message_body = {}
    data_products = []
    for changed_file in changed_files:
        if changed_file.split('/')[-1] == 'domain.yaml':
            message_body['domain'] = parse_domain_yaml(changed_file)
        elif changed_file.split('/')[-1] == 'data_product.yaml':
            data_products.append(parse_data_product_yaml(changed_file))
    message_body['data_products'] = data_products
    send(message_body)
