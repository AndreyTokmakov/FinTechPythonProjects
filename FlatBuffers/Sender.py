
import flatbuffers

from FlatBuffers.model.messaging import Message
from FlatBuffers.model.messaging.Message import Message as MessageClass
from FlatBuffers.model.messaging import Status

# https://flatbuffers.dev/tutorial/#python

if __name__ == "__main__":
    # Construct a Builder with 1024 byte backing array.
    builder = flatbuffers.Builder(1024)

    name = builder.CreateString('Some_Test_Name')

    # Create message
    Message.Start(builder)
    Message.AddName(builder, name)
    Message.AddId(builder, 123)
    Message.AddStatus(builder, Status.Status().Success)

    msg = Message.End(builder)
    builder.Finish(msg)

    data: bytearray = builder.Output()

    # print(msg)
    #  print(data)

    message: Message = MessageClass.GetRootAs(data, 0)
    print(f'Message(name: "{message.Name().decode()}", id: {message.Id()}, status: {message.Status()})')
