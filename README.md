> **Scientific value:** This project is subject to a thesis I write/wrote in 10th grade of my school career.
You can find the thesis relevant documents under `science/` as soon as the writing is completed 🙌<br>
The paper addresses the possibility of replacing global freight shipment with autonomous sailing vessels
which would only transport small amounts of cargo but though could be environmentally friendly and save costs of crew. 

![Boat in action](http://cosmicsail.online/bg.JPG)

# ⛵️ CosmicSail

A while ago I found an old rusty rc sailboat on my attic without any controls or batteries.
So I decided to create a control software which works over the internet, enables autonomous sailing
and makes this boat as cool and advanced as possible :)

At first I went over a few ordinary systems with radio control, but
I noticed very quickly that the problem with those radio controls is that they lose signal after about 50 meters.
In my case that may was related to the antennas being located somewhat below the waterline, blocking the signal.

That was a bit disappointing but nevertheless I searched for a better solution and
came up with the idea of controlling the boat and its motors with a Raspberrypi, 
connected to the internet over cellular network with autonomous capabilities.
For a deployment on larger lakes or even the ocean a satellite connection certainly would be more reliable than an ordinary cellular connection. 
A bigger boat could perhaps even use the [Starlink](https://www.starlink.com) internet service enabling masses of realtime data to be transmitted.

## 📡 Connectivity

As I had to discover, you *cannot* open a WebSocket server from cellular network. This required me to use a proxy server,
instead of a direct connection to the boat. All the realtime transmission happens over Socket.io which is
adopted by frameworks for many different languages. Here is a simple connection diagram:

```markdown
**🎮 Client/Phone** ↔️ **📟 Proxy/Server** ↔️ **⛵️ Boat**
      Svelte                 Golang             Python
```

## 🎚 Hardware

**Sail and Rudder**<br>
Those two motors are servo motors which can be easily controlled via PWM signals from the Raspberry.

**Motor**<br>
The main engine requires a bit more power than the raspberry can provide,
so I first decided to use a L293D microcontroller with external AA batteries.
Sadly the L293D isn't actually rated for the power my motor requires,
so it got hot after a few minutes of driving and even melted parts of the breadboard it was mounted to 🔥
Since then I've replaced the L293D with a professional motor controller, the
[WP1060](https://www.krickshop.de/Elektronik-Motoren/RC-Fernsteuerungen-Zubehoer/Elektronische-Fahrtregler/Fahrtregler-Quicrun-WP1060-Brushed.htm?a=article&ProdNr=67051&p=350) which fortunately, like the servos, can be controlled with PWM Signals.

**PWM Signals**<br>
Emitting PWM Signals from the Pi is very easy, but because it does use a digital clock cycle, the signal can be fuzzy.
Furthermore, the amount of concurrent signals you can emit from the Pi is very limited.
I am currently using the [PCA9685](https://www.adafruit.com/product/815) with 16 channels.
It resolves all the issues of PWM Signals emitted directly from the Pi.

**Sensors**<br>
A Neo6M GPS-Module from ublox in conjunction with their AGPS service is used to get accurate position data in a matter of seconds. 
However, the heading that the gps provides is very dependent on it's speed and accuracy. 
Therefore, a BNO055 9-axis IMU provides heading and even roll as well as pitch with compensation for 
magnetic field disturbances created by motors in the boat.<br>

In addition to the physical sensors, the boat also
contains software to read wind data from the OpenWeatherMap api and uses onwater.io to detect shores. 
This is especially useful when tracking against the wind because it provides the capability of automatic turning, should the boat get too close to the shore.
However, this approach contains some negative aspects including only punctual land detection as the onwater.io api only supports point queries and no areas.
This could be improved by storing/downloading shapedata of the lake locally on the boat and checking the current position against that. 
Furthermore, it could even enable automatic routing around landmasses.

**Power**<br>
The raspberrypi and with it the servos as well as the sensors are powered by a pretty standard big powerbank,
providing enough power for hours of sailing. The motor, is powered by a [LiPo 2S 7.4V/1500mAh](https://www.krickshop.de/Elektronik-Motoren/Akkus-Ladetechnik/LiPo-Akku-7-4V-1500-mAh-15-C.htm?a=article&ProdNr=646090&p=365) battery.

## 🤖 Autopilot

As of now, the forces on sails that the boat experiences in the real world can be simulated 
right on the raspberrypi inside the boat and a first version of the autopilot is fully functional, 
including sailing with and against the wind and maneuvering with the motor. 
There may be some bugs hidden in the code and the boat has to be extensively tested on lakes, 
but it's working perfectly autonomous in the simulation right now. 
A more detailed description of what's going on inside the autopilot will be available soon!

## 🚧 Going further

If you are interested, you can look into our [Documentation](./docs)

I am grateful for any type of feedback, inspiration or question regarding CosmicSail.<br>
Feel free to create an issue or mail me to get in touch.

