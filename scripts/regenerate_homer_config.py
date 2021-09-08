#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  import os
  import time
  import ruamel.yaml
  import signal
  import sys
  from blessed import Terminal
  
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from deps.consts import volumesDirectory, servicesDirectory, templatesDirectory, buildSettingsFileName, buildCache, servicesFileName
  from deps.common_functions import getExternalPorts, getInternalPorts, checkPortConflicts, enterPortNumberWithWhiptail, generateRandomString

  yaml = ruamel.yaml.YAML()
  yaml.preserve_quotes = True

  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring

  # runtime vars
  portConflicts = []
  currentServiceName = 'homer'
  serviceVolume = volumesDirectory + currentServiceName  + '/'
  serviceService = servicesDirectory + currentServiceName  + '/'
  serviceTemplate = templatesDirectory + currentServiceName  + '/'
  serviceConfigFile = 'config.dist.yml'


  with open(buildCache) as objdockerComposeServicesFile:
      dockerComposeServicesYaml = yaml.load(objdockerComposeServicesFile)
  
  with open(serviceTemplate + serviceConfigFile) as objServiceConfigFile:
      serviceConfigFile = yaml.load(objServiceConfigFile)

  ipOfHost = get_ip_address()

  listOfApplication = []
  # TODO: find a why to only like http urls
  for service in dockerComposeServicesYaml['services']:
      ports = [ x.split(':')[0] for x in dockerComposeServicesYaml['services'][service]['ports']]
      listOfApplication.append({
      'name':service,
      'logo':'assets/tools/sample.png',
      'subtitle': (' ' + ipOfHost + ':').join(ports),
      'tag': "http://" + ipOfHost + ':'+ dockerComposeServicesYaml['services'][service]['ports'][0].split(':')[0],
      'url': "http://" + ipOfHost + ':'+ dockerComposeServicesYaml['services'][service]['ports'][0].split(':')[0],
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
