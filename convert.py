import csv
import json
import sys
from pathlib import Path

""""
This code provided by: Osama Bany Hamad
"""


class InvalidCommand(Exception):
    pass


class InvalidFilePath(Exception):
    pass


def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        clients = {}
        for row in csv_reader:
            client_id = row['client_id']
            if client_id not in clients:
                clients[client_id] = {'id': client_id, 'name': row['name'], 'email': row['email'],
                                      'phone': row['phone'], 'accounts': []}
            account = {'id': row['account_id'], 'type': row['type'], 'balance': row['balance'], 'cards': []}
            if account not in clients[client_id]['accounts']:
                clients[client_id]['accounts'].append(account)
            card = {'id': row['card_id'], 'type': row['card_type'], 'expiry_date': row['expiry_date'],
                    'credit_limit': row['credit_limit']}
            if card not in account['cards']:
                account['cards'].append(card)

        clients_list = list(clients.values())

    json_file_path = Path(json_file_path.parent, "converted_" + json_file_path.name)

    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(clients_list, json_file, indent=4)


def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        clients = json.load(json_file)

    csv_file_path = Path(csv_file_path.parent, "converted_" + csv_file_path.name)

    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['client_id', 'name', 'email', 'phone', 'account_id', 'type', 'balance', 'card_id', 'card_type',
                      'expiry_date', 'credit_limit']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for client in clients:
            for account in client.get('accounts', []):
                for card in account.get('cards', []):
                    row = {
                        'client_id': client['id'],
                        'name': client['name'],
                        'email': client['email'],
                        'phone': client['phone'],
                        'account_id': account['id'],
                        'type': account['type'],
                        'balance': account['balance'],
                        'card_id': card['id'],
                        'card_type': card['type'],
                        'expiry_date': card['expiry_date'],
                        'credit_limit': card['credit_limit']
                    }
                    csv_writer.writerow(row)


def main(file_path):
    path = Path(file_path)

    if not path.exists():
        raise InvalidFilePath("File does not exist.")

    if path.suffix.lower() == '.csv':
        json_file_path = path.with_suffix('.json')
        csv_to_json(file_path, json_file_path)

        print(f"Converted CSV to JSON: {json_file_path}")
    elif path.suffix.lower() == '.json':
        csv_file_path = path.with_suffix('.csv')
        json_to_csv(file_path, csv_file_path)
        print(f"Converted JSON to CSV: {csv_file_path}")

    else:
        raise InvalidFilePath("Unsupported file format. Please provide a CSV or JSON file.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise InvalidCommand("The command syntax must be: python convert.py <file_path>")
    else:
        path = sys.argv[1]
        main(path)
