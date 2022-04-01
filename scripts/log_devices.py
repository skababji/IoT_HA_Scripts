from asyncore import write
from html import entities
import appdaemon.plugins.hass.hassapi as hass
import csv


class LogDevices(hass.Hass):

  def initialize(self):
    # This module logs the status of selected devices (defined in ent_names) to a locally stored file (output_file) every minute
    self.log("Started Module LogDevices")
    output_file = '/config/your_log_file_name.csv'

    ent_names=[
      "time_stamp"
      ,"binary_sensor.flood_west_flood"
      ,"binary_sensor.inverted_garage_sensor"
      ,"binary_sensor.shellyflood_xxx1_flood"
      ,"binary_sensor.shellyflood_xxx2_flood"
      ,"binary_sensor.shellyflood_xxx3_flood"
      ,"sensor.openweathermap_cloud_coverage"
      ,"sensor.openweathermap_temperature"
      ,"sensor.phase_1_current"
      ,"sensor.phase_1_power_factor"
      ,"sensor.phase_1_voltage"
      ,"sensor.phase_2_current"
      ,"sensor.phase_2_power_factor"
      ,"sensor.phase_2_voltage"
      ,"switch.amplifier_socket_1"  
    ]

    with open(output_file,'a+') as f:
      writer = csv.writer(f,dialect='unix')
      writer.writerow(ent_names) #write header
    self.log("Wrote Header to file : " + output_file)
    time_stamp=self.get_now()
    self.run_minutely(self.write_states, time_stamp, ent_names=ent_names, output_file=output_file)

  def write_states(self, kwargs):
      time_stamp=self.get_now()
      ent_names=kwargs['ent_names']
      output_file=kwargs['output_file']
      entity_states=[time_stamp]

      for i in range(1,len(ent_names)):
        this_ent=self.get_entity(ent_names[i])
        state=this_ent.get_state()
        entity_states.append(state)
      
      with open(output_file,'a') as f:
        writer = csv.writer(f,dialect='unix')
        writer.writerow(entity_states) 




 









   