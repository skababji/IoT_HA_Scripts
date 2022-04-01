This repo includes sample Python scripts developed using [Appdaemon ](https://appdaemon.readthedocs.io/en/latest/)for [Home Assistant](https://www.home-assistant.io/) (HA)). You may copy and customize the scripts to your needs.

To run the scripts, you are expected to have HA [installed ](https://www.home-assistant.io/installation/)on your hub of choice. You then need to install Appdaemon as an add-on to HA. You may need to check a [video ](https://www.youtube.com/watch?v=GVIS7GtqLpo&t=326s)for the necessary setup.

Once everything is installed, you need to customize the sample scripts to your needs. Each script is self-explanatory and includes basic comments to enhance readability.  The scripts include calling some APIs, playing tracks, checking various sensors, writing selected sensor states to local file and executing other actions. It is unlikely, you have the same sensors, however, you can easily install these by searching HA HACS community.

Below are general guidelines you may consider when customizing the scripts:

* For media_content_id, you need to enter the full URL. For instance, if you are playing a local mp3 file stored in the hub of your choice (e.g. [Rasperry Pi 3B+](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)), you need to make sure that the track is stored under the folder: /config/www/ and in the script enter the full URL, e.g. "https://HA-IP-ADDRESS/local/TRACK_FILE_NAME.mp3"
* HA-IP-ADDRESS could be either your local ip address of the hub or, if you are using DNS service (e.g. duckdns), your domain name. Make sure to add :8123 after the domain name.
