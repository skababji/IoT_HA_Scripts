import appdaemon.plugins.hass.hassapi as hass

class GFLamps(hass.Hass):
    def initialize(self):
        # This module turns on ground floor lights daily based on the weather condition (cloud coverage) and sunset time.
        self.log("Started Module for Ground Floor Lamps! ")
        self.run_daily(self.check_clouds, "sunset - 01:05:00")


    def check_clouds(self, kwargs):
        cloud_cover=self.get_state(entity_id="sensor.openweathermap_forecast_cloud_coverage", attribute=None, default=None, copy=True)
        self.log("Fecthed Cloud COVERAGE {} !".format(cloud_cover))
        if int(cloud_cover)>=90:
            self.run_daily(self.turn_on_gflights, "sunset - 01:00:00")
        elif 75<int(cloud_cover)<90:
            self.run_daily(self.turn_on_gflights, "sunset - 00:45:00")
        else:
            self.run_daily(self.turn_on_gflights, "sunset - 00:20:00")


    def turn_on_gflights(self,kwargs):
            self.turn_on("switch.tv_right_socket_1")
            self.turn_on("switch.tv_left_socket_1")
            self.turn_on("switch.hallway_lamps_socket_1")
            self.log("Ground floor lamps are turned on")

