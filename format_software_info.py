import os
import sys
import yaml
import re
#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
SOFTWARE_DIR='software'
SOFTWARE_DOCS='docs/applications/'
#-------------------------------------------------------------------------------
# get files and folder names of folder dirpath
def getDirectoryList(dirpath,mask):
  files=[]
  dirs=[]
  for file in os.listdir(dirpath):
    if os.path.isdir(os.path.join(dirpath, file)):
      dirs.append(os.path.join(dirpath, file))
    else:
      files.append(os.path.join(dirpath, file))
  return sortSoftware(dirs,mask),files
#-------------------------------------------------------------------------------
# Sort the names of files according to version number or text
# Only takes into consideration the name and not the filepath
def sortSoftware(files,mask):
  if len(mask)>0:
    files.sort(key=lambda s: list(map(int,filter(None,re.split(mask,os.path.basename(s))))))
  else:
    files.sort(key=lambda s: list(os.path.basename(s)))
  return files
#-------------------------------------------------------------------------------
# Write keywords from keywords.yml to beginning of markdown file
def writeKeywords(software,fp,keywords):
  if not os.path.isfile(os.path.join(SOFTWARE_DIR, software, "keywords.yaml")):
    keywords['misc'].append(software)
    return
  fp.write("---\n")
  fp.write("title: Information about %s\n" % (software))
  fp.write("keywords:\n")
  with open(os.path.join(SOFTWARE_DIR, software, "keywords.yaml"), 'r') as file:
    yaml_data = yaml.safe_load(file)
  for value in yaml_data['keywords']:
    fp.write("  - %s\n" % (value))
    if value not in keywords:
      keywords[value]=[]
    if software not in keywords[value]:
      keywords[value].append(software)
  fp.write("---\n")
#-------------------------------------------------------------------------------
# Check if software is installed on active clusters
def checkSoftware(softwarename,clusters):
  found=False
  if not os.path.isfile(os.path.join(SOFTWARE_DIR, softwarename, "versions.yaml")):
    return found
  with open(os.path.join(SOFTWARE_DIR, softwarename, "versions.yaml"), 'r') as file:
    yaml_data = yaml.safe_load(file)
  if yaml_data is None:
    return found
  if "resources" not in yaml_data:
    return found
  for resource in yaml_data['resources']:
    if getClusterText(resource['resource'],clusters)!="":
      found=True
  return found
#-------------------------------------------------------------------------------
# Write which versions of the software are installed
def writeVersions(softwarename,clusters,fp,fpidx):
  with open(os.path.join(SOFTWARE_DIR, softwarename, "versions.yaml"), 'r') as file:
    yaml_data = yaml.safe_load(file)
  fp.write("\n## Installed versions\n\n")
  fp.write("| Resource | Version |\n|---|---|\n")
  fpidx.write("| [%s](%s) | " % (softwarename.capitalize(),os.path.join(softwarename,"index.md")))
  firstidx=True
  for resource in yaml_data['resources']:
    cluster=getClusterText(resource['resource'],clusters)
    if cluster=="":
      continue
    if not firstidx:
      fpidx.write("|| ")
    firstidx=False
    fp.write("| %s | " % (cluster))
    fpidx.write("%s | " % (cluster))
    if isinstance(resource['versions'], list):
      versionname=[]
      for version_info in resource['versions']:
        versionname.append(str(version_info['version']))
      fp.write(", ".join(versionname))
      fpidx.write(", ".join(versionname))
    fpidx.write(" |\n")
    fp.write(" |\n")
  fp.write("\n")
#-------------------------------------------------------------------------------
# Write general information about the software
def appendGeneralInfo(softwarename,fp):
  if not os.path.isfile(os.path.join(SOFTWARE_DIR,softwarename,"general.md")):
    return
  fp2=open(os.path.join(SOFTWARE_DIR,softwarename,"general.md"),"r")
  fp.write("## General information\n\n")
  for line in fp2:
    fp.write(line)
  fp2.close()
  fp.write("\n")
#-------------------------------------------------------------------------------
# Check if this is an active cluster
def getClusterText(resource,clusters):
  for cluster in clusters:
    if cluster['cluster'] == resource:
      return resource
    if not 'env' in cluster:
      continue
    if cluster['env'] == resource:
      return cluster['cluster']+"/"+resource
  return ""
#-------------------------------------------------------------------------------
# Write the YAML file with categories and software
def writeYAMLMenu(keywords):
  fp=open("mkdocs.yaml","a")
  keywords=dict(sorted(keywords.items()))
  for key in keywords:
    keywords[key].sort()
    fp.write("    - %s:\n" % (key.capitalize()))
    for value in keywords[key]:  
      fp.write("      - %s: %s\n" % (value.capitalize(),os.path.join("applications",value,"index.md")))
  fp.close()
#-------------------------------------------------------------------------------
def main():
  os.system("cp template/mkdocs.yaml .")
  os.system("mkdir -p %s" % (SOFTWARE_DOCS,))
  os.system("cp template/index.md %s" % (SOFTWARE_DOCS,))
  with open("clusters.yaml", 'r') as file:
    clusters = yaml.safe_load(file)
  softwares,files=getDirectoryList(SOFTWARE_DIR,'')
  fpidx=open(SOFTWARE_DOCS+"/index.md","a")
  keywords={}
  keywords['misc']=[]
  for software in softwares:
    softwarename=os.path.basename(software)
    if not checkSoftware(softwarename,clusters):
      continue
    os.system("mkdir -p %s" % (os.path.join(SOFTWARE_DOCS,softwarename)))
    if os.path.isdir(os.path.join(SOFTWARE_DIR,softwarename,"files")):
      os.system("cp -r %s/files %s" % (os.path.join(SOFTWARE_DIR,softwarename),os.path.join(SOFTWARE_DOCS,softwarename)))
    file=os.path.join(SOFTWARE_DOCS,softwarename,"index.md")
    fp=open(file,"w")
    writeKeywords(softwarename,fp,keywords)
    fp.write("# %s\n" % (softwarename.capitalize()))
    writeVersions(softwarename,clusters,fp,fpidx)
    appendGeneralInfo(softwarename,fp)
    fp.close()
  fpidx.close()
  writeYAMLMenu(keywords)
#-------------------------------------------------------------------------------
if __name__ == '__main__':
  main()
