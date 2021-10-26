from pushbullet import Pushbullet

pb = Pushbullet("o.V5Jqi0GFHQuwjaysXbTmBzK4Mdt1scbm")
channel = pb.channels[0]
channel.push_note("Hello Channel!", "Hello My Channel")
