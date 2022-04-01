import appdaemon.plugins.hass.hassapi as hass
import datetime
import requests


class MakeAzan(hass.Hass):
    def initialize(self):
        # This module convert today's date into Hijri date by calling an API, retrieves Islamic prayer times from a sensor (available as HA integration), 
        # allows the user to offset the fetched time, and daily announces the Azan for the five prayers through connected speakers. In Ramadan, 
        # special recitations are launched before the Iftar time. 

        self.log("Started Make Azan")

        today=self.get_state(entity_id="sensor.date", attribute=None, default=None, copy=True)
        today_hijri,hijri_month,hijri_day=self.get_hijri(today)
        self.log("TODAY = {}R = {}H".format(str(today),str(today_hijri)))
        self.log("Day in Hijri = {}".format(str(hijri_day)))
        self.log("Month in Hijri = {}".format(str(hijri_month)))

        #Zuhr Azan
        zuhr=self.get_state(entity_id="sensor.dhuhr_prayer", attribute=None, default=None, copy=True)
        zuhr_time=self.parse_time(zuhr,60*5,0)
        self.run_daily(self.announce_track, zuhr_time, entity_id="media_player.speaker_entity_id",volume_level=0.2,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/azan.mp3")

        # Asr Azan
        asr=self.get_state(entity_id="sensor.asr_prayer", attribute=None, default=None, copy=True)
        asr_time=self.parse_time(asr,60*5,0)
        self.run_daily(self.announce_track, asr_time, entity_id="media_player.speaker_entity_id",volume_level=0.2,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/azan.mp3")

        # Maghrib Azan
        maghrib=self.get_state(entity_id="sensor.maghrib_prayer", attribute=None, default=None, copy=True)
        if hijri_month==9:# if it is ramadan
            self.log('It is Ramadan!')     
            if hijri_day%2==0: #Tracks to play in even days of Ramadan
                ramadan_zikr_time=self.parse_time(maghrib,60*10, 245)
                self.run_daily(self.announce_track, ramadan_zikr_time, entity_id="media_player.speaker_entity_id",volume_level=0.3,
                    media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/ebtehal1.mp3")
            else: #Tracks to play in odd days of Ramadan
                ramadan_zikr_time=self.parse_time(maghrib,60*10, 245)
                self.run_daily(self.announce_track, ramadan_zikr_time, entity_id="media_player.speaker_entity_id",volume_level=0.3,
                    media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/ebtehal2.mp3")  
            
            maghrib_time=self.parse_time(maghrib, 60*10,0)
            self.run_daily(self.announce_track, maghrib_time, entity_id="media_player.speaker_entity_id",volume_level=0.3,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/ramadan_azan.mp3")
        else:
            maghrib_time=self.parse_time(maghrib, 60*10,0)
            self.run_daily(self.announce_track, maghrib_time,entity_id="media_player.speaker_entity_id",volume_level=0.2,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/azan.mp3")

        # Isha Azan
        isha=self.get_state(entity_id="sensor.isha_prayer", attribute=None, default=None, copy=True)
        isha_time=self.parse_time(isha,60*5,0)
        self.run_daily(self.announce_track, isha_time,entity_id="media_player.speaker_entity_id",volume_level=0.2,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/azan.mp3")

        # Fajr Azan
        fajr=self.get_state(entity_id="sensor.fajr_prayer", attribute=None, default=None, copy=True)
        fajr_time=self.parse_time(fajr,60*5,0)
        self.run_daily(self.announce_track, fajr_time,entity_id="media_player.speaker_entity_id",volume_level=0.2,
                media_content_type="mp3",media_content_id="https://HA-IP-ADDRESS/local/fajr_azan.mp3") 
  
    
    def parse_time(self,event_utc, sec_add, sec_subtract): #sec_add and sec_subtract are offsets in seconds 
        event=self.parse_utc_string(event_utc)+self.get_tz_offset()
        event=event+sec_add-sec_subtract 
        event = datetime.datetime.fromtimestamp(event).time()
        return event

    def get_hijri(self, inp_date):
        #A function that returns hijri date, day and month
        inp_date=str(inp_date)
        inp_date=datetime.datetime.strptime(inp_date, '%Y-%m-%d').strftime('%d-%m-%Y') #convert date into a API's rquired format
        req =requests.get('http://api.aladhan.com/v1/gToH?date='+str(inp_date))
        req_in_json=req.json()
        self.log('{}'.format(str(req_in_json['data']['hijri'])))
        hijri_date=req_in_json['data']['hijri']['date']
        hijri_month=req_in_json['data']['hijri']['month']['number']
        hijri_day=int(req_in_json['data']['hijri']['day'])
        return hijri_date,hijri_month, hijri_day
    
# Call backs

    def announce_track(self,kawrgs):
        self.log("Input track is launched!")
        #set volume
        self.call_service("media_player/volume_set",entity_id = kawrgs['entity_id'], volume_level=kawrgs['volume_level'])
        #start track
        self.call_service("media_player/play_media",entity_id = kawrgs['entity_id'], 
            media_content_id=kawrgs['media_content_id'],media_content_type=kawrgs['media_content_type'])



