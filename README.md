## Microsoft© Azure SDK for Python

Made for [netPI RTE 3](https://www.netiot.com/netpi/), the Raspberry Pi 3B Architecture based industrial suited Open Edge Connectivity Ecosystem

### PROFINET device scanner pushing browsed device data to Microsoft Azure IoT Hub using Python SDK

The image provided hereunder deploys a container with an installed PROFINET device scanner browsing for devices connected to netPI RTE 3's switched Industrial Ethernet ports and pushing the accumulated scanned device data to a given Microsoft Azure IoT Hub as a JSON formatted string with Python SDK

Base of this image builds [debian](https://www.balena.io/docs/reference/base-images/base-images/) with installed python3 language interpreter, a Python based scanner script and Microsoft's Python based [Azure Client SDK](https://azure.microsoft.com/en-us/downloads/).

#### Use with Hilscher's demo showcase

Use the container in conjunction with Hilscher's MS Azure based dashboard located at [netPI-di-portal](http://netpi.di-portal.com/). 

1. Get a personal connection string for a private session using an email address as reference [here](http://netpi.di-portal.com/Registration). Use the provided primary connection string as environment variable `IOTHUB_CONNECTION_STRING` for the container. 

2. Visit the [dashboard](http://netpi.di-portal.com/Dashboard) and enter your email reference as DeviceID again to get to your private dashboard.

3. Watch the list of detected devices rolling in. Click `Sync with DI-Portal` to initiate a synchronisation process between the dashboard and the DI-portal. Corresponding informations found on DI-Portal will be then replaced by human readable values in the device list.

4. If no informations are available you can upload those to the DI-portal yourself. This requires an DI-Portal account. There you can upload the informations either globally available to everybody or on a private hidden basis just for the demo.
 
The demo is a practical way to understand the use of the DI-Portal and its value for Enterprise Cloud, Industry 4.0 and Internet of Things applications of the automation sector if there is a global database hosting device descriptions centralized to maintain your assets from all over the world.

Watch video demonstation on youtube [netPI - DI-Portal Showcase](https://www.youtube.com/watch?v=NyCEkRAFEa4).

#### Use with your personal MS Azure account

1. Visit [Microsoft Azure](https://azure.microsoft.com) and login if you have an existing account, otherwise register and sign up. In latter case a MS Azure 30 days trial period is offered to newcomers for free. 

2. Switch to [Azure Portal](https://portal.azure.com/) and create a new IoT Hub using `+New`and then`Internet of Things(IoT)`and then`IoT Hub`. Open the IoT Hub and click `Device Explorer` and then `+Add`. Enter a device name in `Device ID` box and click save. 

3. Click the device and locate its `Connection string - primary key`. Use this connection string as environment variable `IOTHUB_CONNECTION_STRING` for the container.

#### Container prerequisites

##### Privileged mode

The container creates a standard Ethernet network interface (LAN) with netPI's Industrial Network Controller netX the scanner script runs the scan procedure across. Creating a LAN needs full access to the Docker Host. Only the privileged mode option lifts the enforced container limitations to allow creation of such a network interface.

##### Host devices

To grant access to the netX from inside the container the `/dev/spidev0.0` host device needs to be exposed to the container.

To allow the container creating an additional network device for the netX network controller the `/dev/net/tun` host device needs to be expose to the container.

##### Environment Variables

Personalize the container with following environment variables:

* **IOTHUB_CONNECTION_STRING** as a reference - also known as connection string - of your Azure IoT Hub

* **FIELDBUS_IP** as IP address of netPI RTE 3's switched Industrial Ethernet ports the scan is made across (same subnet)

#### Getting started

STEP 1. Open netPI's landing page under `https://<netpi's ip address>`.

STEP 2. Click the Docker tile to open the [Portainer.io](http://portainer.io/) Docker management user interface.

STEP 3. Enter the following parameters under **Containers > Add Container**

* **Image**: `hilschernetpi/netpi-diportal-api-showcase`

* **Restart policy"** : `always`

* **Runtime > Env** : `name "FIELDBUS_IP" -> value e.g. "192.168.252.10"`and`name "IOTHUB_CONNECTION_STRING" -> value e.g. "HostName=dev-netpi.azure-devices.net;DeviceId=netpi-xxxxxxxx;SharedAccessKey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

* **Runtime > Privileged mode** : `On`

* **Runtime > Devices > add device**: `Host "/dev/spidev0.0" -> Container "/dev/spidev0.0"`

* **Runtime > Devices > add device**: `Host "/dev/net/tun" -> Container "/dev/net/tun"`

STEP 4. Press the button **Actions > Start/Deploy container**

Pulling the image may take a while (5-10mins). Sometimes it takes so long that a time out is indicated. In this case repeat the **Actions > Start container** action.

#### Accessing

The container starts the device scanning and pushing procedure automatically.

See immediate results on your dashboard or your Azure IoT Hub.

#### Automated build

The project complies with the scripting based [Dockerfile](https://docs.docker.com/engine/reference/builder/) method to build the image output file. Using this method is a precondition for an [automated](https://docs.docker.com/docker-hub/builds/) web based build process on DockerHub platform.

DockerHub web platform is x86 CPU based, but an ARM CPU coded output file is needed for Raspberry systems. This is why the Dockerfile includes the [balena](https://balena.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/) steps.

#### License

View the license information for the software in the project. As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc from the base distribution, along with any direct or indirect dependencies of the primary software being contained).
As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses for all software contained within.

[![N|Solid](http://www.hilscher.com/fileadmin/templates/doctima_2013/resources/Images/logo_hilscher.png)](http://www.hilscher.com)  Hilscher Gesellschaft fuer Systemautomation mbH  www.hilscher.com
