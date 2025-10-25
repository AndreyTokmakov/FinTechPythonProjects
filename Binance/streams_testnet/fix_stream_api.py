import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def logon_raw_data(private_key: Ed25519PrivateKey,
                   sender_comp_id: str,
                   target_comp_id: str,
                   msg_seq_num: str,
                   sending_time: str):
    """
    Computes the value of RawData (96) field in Logon<A> message.
    """
    payload = chr(1).join([
        'A',
        sender_comp_id,
        target_comp_id,
        msg_seq_num,
        sending_time,
    ])

    signature = private_key.sign(payload.encode('ASCII'))

    print(signature)

    return base64.b64encode(signature).decode('ASCII')


def get_private_key():
    with open('/home/andtokm/Documents/Binance/ssh_Key/ed25519.pem', 'rb') as f:
        return load_pem_private_key(data=f.read(), password=None)


if __name__ == "__main__":
    timestamp: str = '20250528-03:56:26.557'
    raw_data = logon_raw_data(get_private_key(),
                              sender_comp_id='100500',
                              target_comp_id='SPOT',
                              msg_seq_num='1',
                              sending_time=timestamp)

    print(raw_data)
