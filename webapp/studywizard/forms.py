# 
# Funf: Open Sensing Framework
# Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
# Acknowledgments: Alan Gardner
# Contact: nadav@media.mit.edu
# 
# This file is part of Funf.
# 
# Funf is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# Funf is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with Funf. If not, see <http://www.gnu.org/licenses/>.
# 
from django import forms

class CreateAppForm(forms.Form):
    #General
    app_name = forms.CharField(max_length=64)
    contact_email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)
    #icon goes here
    #Reg Info (not incorporated in app)
    creator_name_REG_INFO = forms.CharField(max_length=200, required=False)
    creator_email_REG_INFO = forms.EmailField(required=False)
    org_name_REG_INFO = forms.CharField(max_length=200, required=False)
    location_REG_INFO = forms.CharField(max_length=200,required=False)
    #Device
    dataUploadStrategy = forms.ChoiceField(required=True, choices=(('ANY', 'Over Wi-Fi or mobile network'),
                                                                   ('WIFI', 'Over Wi-Fi only'),
                                                                   ('NONE', 'No automatic upload'),
                                                                   ))
    AndroidInfoProbe = forms.BooleanField(required=False)
    AndroidInfoProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    AccountsProbe = forms.BooleanField(required=False)
    AccountsProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ProcessStatisticsProbe = forms.BooleanField(required=False)
    ProcessStatisticsProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ServicesProbe = forms.BooleanField(required=False)
    ServicesProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    BatteryProbe = forms.BooleanField(required=False)
    BatteryProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    HardwareInfoProbe = forms.BooleanField(required=False)
    HardwareInfoProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    TelephonyProbe = forms.BooleanField(required=False)
    TelephonyProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    #TimeOffsetProbe = forms.BooleanField(required=False)
    #TimeOffsetProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    #Device Interaction
    AudioMediaProbe = forms.BooleanField(required=False)
    AudioMediaProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    BrowserBookmarksProbe = forms.BooleanField(required=False)
    BrowserBookmarksProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    BrowserSearchesProbe = forms.BooleanField(required=False)
    BrowserSearchesProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ImageMediaProbe = forms.BooleanField(required=False)
    ImageMediaProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ApplicationsProbe = forms.BooleanField(required=False)
    ApplicationsProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    RunningApplicationsProbe = forms.BooleanField(required=False)
    RunningApplicationsProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    VideoMediaProbe = forms.BooleanField(required=False)
    VideoMediaProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ScreenProbe = forms.BooleanField(required=False)
    #Environment
    AudioFeaturesProbe = forms.BooleanField(required=False)
    AudioFeaturesProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    AudioFeaturesProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    LightSensorProbe = forms.BooleanField(required=False)
    LightSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    LightSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    MagneticFieldSensorProbe = forms.BooleanField(required=False)
    MagneticFieldSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    MagneticFieldSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    PressureSensorProbe = forms.BooleanField(required=False)
    PressureSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    PressureSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    ProximitySensorProbe = forms.BooleanField(required=False)
    ProximitySensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ProximitySensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    TemperatureSensorProbe = forms.BooleanField(required=False)
    TemperatureSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    TemperatureSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    #Motion
    AccelerometerFeaturesProbe = forms.BooleanField(required=False)
    AccelerometerFeaturesProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    AccelerometerFeaturesProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    AccelerometerSensorProbe = forms.BooleanField(required=False)
    AccelerometerSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    AccelerometerSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    ActivityProbe = forms.BooleanField(required=False)
    ActivityProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ActivityProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    GravitySensorProbe = forms.BooleanField(required=False)
    GravitySensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    GravitySensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    GyroscopeSensorProbe = forms.BooleanField(required=False)
    GyroscopeSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    GyroscopeSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    LinearAccelerationSensorProbe = forms.BooleanField(required=False)
    LinearAccelerationSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    LinearAccelerationSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    OrientationSensorProbe = forms.BooleanField(required=False)
    OrientationSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    OrientationSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    RotationVectorSensorProbe = forms.BooleanField(required=False)
    RotationVectorSensorProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    RotationVectorSensorProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    #Positioning
    LocationProbe = forms.BooleanField(required=False)
    LocationProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    LocationProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    SimpleLocationProbe = forms.BooleanField(required=False)
    SimpleLocationProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    SimpleLocationProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    BluetoothProbe = forms.BooleanField(required=False)
    BluetoothProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    BluetoothProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    CellTowerProbe = forms.BooleanField(required=False)
    CellTowerProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    CellTowerProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    WifiProbe = forms.BooleanField(required=False)
    WifiProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    WifiProbe_duration = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_dur',}))
    #Social
    CallLogProbe = forms.BooleanField(required=False)
    CallLogProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    ContactProbe = forms.BooleanField(required=False)
    ContactProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    SMSProbe = forms.BooleanField(required=False)
    SMSProbe_freq = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'size': '5', 'class': 'form_freq',}))
    #Read terms and conditions
    ReadTermsAndConditions = forms.BooleanField(required=True)