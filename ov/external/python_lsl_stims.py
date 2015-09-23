import numpy, sys, os
from math import ceil

# FIXME absolute path to point to pylsl.py
# WARNING: on linux plateforme the library should come from openvibe othewise crashes (??) -- eg: openvibe-1.0.1-src/dependencies/lib/liblsl.so
sys.path.append("/home/jfrey/match/repo/lib/lsl_ov")
from pylsl import StreamInlet, resolve_stream, local_clock

# NB: if case of several streams and/or several channels, every stim will be concatenated

# let's define a new box class that inherits from OVBox
class MyOVBox(OVBox):
  def __init__(self):
    OVBox.__init__(self)

    
  # the initialize method reads settings and outputs the first header
  def initialize(self):
    self.initLabel = 0
    self.debug=self.setting['debug'] == "true"
    print "Debug: ", self.debug
    self.stream_type=self.setting['Stream type']
    self.stream_name=self.setting['Stream name'] 
    # total channels for all streams
    self.channelCount = 0
    #self.stream_name=self.setting['Stream name'] # in case !all_streams
    print "Looking for streams of type: " + self.stream_type
    streams = resolve_stream('type',self.stream_type)
    print "Nb streams: " + str( len(streams))
    self.nb_streams = len(streams)
    if self.nb_streams == 0:
      raise Exception("Error: no stream found.")
    self.inlet = StreamInlet(streams[0], max_buflen=1)
    self.info = self.inlet.info()
    self.channelCount = self.info.channel_count()
    print "Stream name: " + self.info.name()
    stream_freq = self.info.nominal_srate()
    if stream_freq != 0:
	  raise Exception("Error: no irregular stream found.")
    # we append to the box output a stimulation header. This is just a header, dates are 0.
    self.output[0].append(OVStimulationHeader(0., 0.))
    self.init = False
  # The process method will be called by openvibe on every clock tick
  def process(self):
    # A stimulation set is a chunk which starts at current time and end time is the time step between two calls
    # init here and filled within triger()
    self.stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
    if self.init == False :
     local_time = local_clock()
     initSecond=int(local_time) 
     initMillis=int((local_time-initSecond)*1000)
     self.stimSet.append(OVStimulation(self.initLabel, self.getCurrentTime(), 0.))
     self.stimSet.append(OVStimulation(initSecond, self.getCurrentTime(), 0.))
     self.stimSet.append(OVStimulation(initMillis, self.getCurrentTime(), 0.))
     self.init=True
	# read all available stream
    samples=[]
    sample,timestamp = self.inlet.pull_sample(0)
    while sample != None:
     samples += sample
     sample,timestamp = self.inlet.pull_sample(0)
     # every value will be converted to openvibe code and a stim will be create
    for label in samples: 
      label = str(label)
      if self.debug:
        print "Got label: ", label
      self.stimSet.append(OVStimulation(float(label), self.getCurrentTime(), 0.))	
    # even if it's empty we have to send stim list to keep the rest in sync
    self.output[0].append(self.stimSet)

  def uninitialize(self):
    # we send a stream end.
    end = self.getCurrentTime()
    self.output[0].append(OVStimulationEnd(end, end))
    self.inlet.close_stream()

box = MyOVBox()
