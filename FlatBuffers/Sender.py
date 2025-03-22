
import flatbuffers

# Generated by `flatc`.
import model.messaging.Message
import model.messaging.Status
from FlatBuffers.model.messaging import Message

# https://flatbuffers.dev/tutorial/#python

if __name__ == "__main__":
    print(1)

    # Construct a Builder with 1024 byte backing array.
    builder = flatbuffers.Builder(1024)

    name = builder.CreateString('Some_Test_Name')

    status = Message.Sta.Color().Red

    # Create message
    Message.Start(builder)
    Message.AddName(builder, name)
    Message.AddId(builder, 5)
    Message.AddStatus(builder, 3)

    msg = Message.End(builder)