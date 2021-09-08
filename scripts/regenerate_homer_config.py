#!/usr/bin/env python3

# Main wrapper function. Required to make local vars work correctly
def main():
  import os
  import time
  #import ruamel.yaml
  import yaml
  import signal
  import sys
  from blessed import Terminal
  
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from deps.consts import dockerPathOutput, volumesDirectory, servicesDirectory, templatesDirectory, buildSettingsFileName, buildCache, servicesFileName
  from deps.common_functions import getExternalPorts, getInternalPorts, checkPortConflicts, enterPortNumberWithWhiptail, generateRandomString

  # yaml = ruamel.yaml.YAML()
  # yaml.preserve_quotes = True

  # runtime vars
  currentServiceName = 'homer'
  serviceVolume = volumesDirectory + currentServiceName  + '/'
  serviceTemplate = templatesDirectory + currentServiceName  + '/'
  serviceConfigFile = 'config.dist.yml'


  with open(dockerPathOutput) as objdockerComposeServicesFile:
      dockerComposeServicesYaml = yaml.load(objdockerComposeServicesFile)
  
  with open(serviceTemplate + serviceConfigFile) as objServiceConfigFile:
      serviceConfigFile = yaml.load(objServiceConfigFile)

  ipOfHost = get_ip_address()

  listOfApplication = []
  # TODO: nicer version, more changed files... ok but need more
  
  for currentServiceName in dockerComposeServicesYaml['services']:
      with open(templatesDirectory + currentServiceName + '/service.yml') as objServiceConfigFile:
        serviceFile = yaml.load(objServiceConfigFile)
      # TODO: figure out how this works with ruaml... or not who cares about the file layou since it is overwritten on every run
      if 'x-homer-port' in serviceFile[currentServiceName].keys():
        httpPort = serviceFile[currentServiceName]['x-homer-port']
        portsList = serviceFile[currentServiceName]['ports']
        ports = [ x.split(':')[0] for x in portsList]
      else:
        continue
      listOfApplication.append({
      'name':currentServiceName,
      'logo':'assets/tools/sample.png',
      'subtitle': ipOfHost + ':'+ (' ' + ipOfHost + ':').join(ports),
      'tag': "http://" + ipOfHost + ':'+ str(httpPort),
      'url': "http://" + ipOfHost + ':'+ str(httpPort),
      #'target': "_blank" # optional html a tag target attribute
  } )

  serviceConfigFile['services'] = [{'name': "Applications",
      'icon': "fas fa-cloud",
      'items': listOfApplication }]
  with open(serviceVolume + 'assets/config.yml', 'w') as objServiceConfigFile:
    serviceConfigFileYaml = yaml.dump(serviceConfigFile, objServiceConfigFile)




def get_ip_address():
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  return s.getsockname()[0]


# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if __name__ == '__main__':
  main()
