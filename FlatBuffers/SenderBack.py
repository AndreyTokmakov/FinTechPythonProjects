
import flatbuffers

# Generated by `flatc`.
import model.MyGame.Sample.Color
import model.MyGame.Sample.Equipment
import model.MyGame.Sample.Monster
import model.MyGame.Sample.Vec3
from FlatBuffers.model.MyGame.Sample import Weapon

# https://flatbuffers.dev/tutorial/#python

if __name__ == "__main__":
    print(1)

    # Construct a Builder with 1024 byte backing array.
    builder = flatbuffers.Builder(1024)

    weapon_two = builder.CreateString('Axe')

    # Create the second `Weapon` ('Axe').
    Weapon.Start(builder)
    Weapon.AddName(builder, weapon_two)
    Weapon.AddDamage(builder, 5)
    axe = Weapon.End(builder)

    print(axe.Name())
    print(axe)

    # Call `Finish()` to instruct the builder that this monster is complete.
    builder.Finish(axe)

    # This must be called after `Finish()`.
    buf: bytearray = builder.Output()

    print(buf)

