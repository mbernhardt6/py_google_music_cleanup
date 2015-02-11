#!/usr/bin/env python
#This version does not check for play count prior to deleting a song.
from gmusicapi import Mobileclient
import argparse

#Parse command line arguments.
parser = argparse.ArgumentParser(description='Process command line flags.')
parser.add_argument('--delete', dest='run_delete', action='store_true', default=False, help='Flag required to run delete command.')
args = parser.parse_args()

if not(args.run_delete):
  print "Missing \"--delete\" flag. Running in logging-only mode."
else:
  print "\"--delete\" flag present. Running in delete mode."

#TODO: Implement a separate password file?
print "Logging in."
api = Mobileclient()
logged_in = api.login('username', 'password')

#Global variables
#TODO: Don't know if these should go here or if I'm just too lazy.
track_set = set()
total_delete = 0
total_skipped = 0

def delete_track(track):
  print " Duplicate:: Title: %s (%s)" % (track['title'], track['artist'])
  total_delete += 1
  if (args.run_delete):
    api.delete_songs(track['id'])

#TODO: Implement "playCount" check as part of function.
#if (track['playCount'] == 0):
#TODO: Implement a scoring system of multiple checks.
#      Each check would add a point.
#      Minimum number of points required to be deleted.
#      Weighted checks worth more points.
def ok_to_delete(track):
  bool_delete = False
  trackId = track['id']
  calculated_string = ((track['title'] + track['artist'] + track['album'] + track['durationMillis']).replace(" ", "")).lower()
  if calculated_string in track_set:
    if (trackId not in trackIds_in_playlists):
      bool_delete = True
    else:
      print "  _In playlist:: Title %s (%s)" % (track['title'], track['artist'])
      total_skipped += 1
      bool_delete = False
  else:
    track_set.add(calculated_string)
    bool_delete = False
  return bool_delete

def find_and_remove_dups(api, tracks):
  #Forward pass
  for track in tracks:
    if ok_to_delete(track):
      delete_track(track)
  #Reset track_set
  track_set.clear()
  #Reverse pass
  for track in reversed(tracks):
    if ok_to_delete(track):
      delete_track(track)
  #Skipped count may be innaccurate due to double pass.
  print "====="
  print "Total Deleted: %d" % total_delete
  if not(args.run_delete):
    print "Logging-only mode. Above number purely informational."
  print "Total Skipped: %d" % total_skipped

def build_songs_in_playlists(api, playlists):
  track_list = set()
  for playlist in playlists:
    for track in playlist['tracks']:
      entryId = track['trackId']
      if entryId not in track_list:
        track_list.add(entryId)
  return track_list

if logged_in:
  print "Gathering all songs."
  full_library = api.get_all_songs()
  print "Gather all playlists."
  all_playlists = api.get_all_user_playlist_contents()
  print "Building collection of songs in playlists."
  trackIds_in_playlists = build_songs_in_playlists(api, all_playlists)
  print "Searching for duplicates."
  find_and_remove_dups(api, full_library)