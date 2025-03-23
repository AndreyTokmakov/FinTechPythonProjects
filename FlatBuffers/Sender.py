import flatbuffers

from FlatBuffers.model.messaging import Message
from FlatBuffers.model.messaging.Message import Message as MessageClass
from FlatBuffers.model.messaging import Status


# https://flatbuffers.dev/tutorial/#python

def build_message(text: str, msg_id: int, status: Status) -> bytearray:
    # Construct a Builder with 1024 byte backing array.
    builder = flatbuffers.Builder(1024)

    name = builder.CreateString(text)

    # Create message
    Message.Start(builder)
    Message.AddText(builder, name)
    Message.AddId(builder, msg_id)
    Message.AddStatus(builder, status)

    msg = Message.End(builder)
    builder.Finish(msg)

    data: bytearray = builder.Output()
    return data


def read_message(msg: Message) -> Message:
    return MessageClass.GetRootAs(msg, 0)


if __name__ == "__main__":
    msg_data: bytearray = build_message(text='Some_Test_Name',
                                        msg_id=12345,
                                        status=Status.Status().Success)
    message: Message = MessageClass.GetRootAs(msg_data, 0)

    print(f'Message(text: "{message.Text().decode()}", id: {message.Id()}, status: {message.Status()})')
