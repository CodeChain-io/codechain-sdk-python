from jsonrpcclient.requests import Request


class Account:
    def __init__(self, client):
        self.client = client

    def get_list(self):
        payload = Request("account_getList")
        response = self.client.send(payload)

        return response.data.result

    def create(self, passphrase):
        payload = Request("account_create", passphrase=passphrase)
        response = self.client.send(payload)

        return response.data.result

    def import_raw(self, secret, passphrase):
        payload = Request("account_importRaw", secret=secret, passphrase=passphrase)
        response = self.client.send(payload)

        return response.data.result

    def unlock(self, account, passphrase):
        payload = Request("account_unlock", account=account, passphrase=passphrase)
        response = self.client.send(payload)

        return response.data.result

    def sign(self, message, account, passphrase):
        payload = Request(
            "account_sign", message=message, account=account, passphrase=passphrase
        )
        response = self.client.send(payload)

        return response.data.result

    def send_transaction(self, transaction, account, passphrase):
        payload = Request(
            "account_sendTransaction",
            transaction=transaction,
            account=account,
            passphrase=passphrase,
        )
        response = self.client.send(payload)

        return response.data.result

    def change_password(self, account, old_passphrase, new_passphrase):
        payload = Request(
            "account_changePassword",
            account=account,
            oldPassphrase=old_passphrase,
            newPassphrase=new_passphrase,
        )
        response = self.client.send(payload)

        return response.data.result
