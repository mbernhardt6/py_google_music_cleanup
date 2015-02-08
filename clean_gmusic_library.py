#!/usr/bin/env python
#This version does not check for play count prior to deleting a song.
from gmusicapi import Mobileclient
import sys

print "Logging in."
api = Mobileclient()
logged_in = api.login('username', 'password')

#TODO: Add a reversed() pass for better tracks_in_playlist avoidance.
def find_and_remove_dups(api, tracks, tracks_in_playlist):
  total_delete = 0
  total_skipped = 0
  track_set = set()
  for track in tracks:
    entryId = track['id']
    calculated_string = ((track['title'] + track['artist'] + track['album'] + track['durationMillis']).replace(" ", "")).lower()
    if calculated_string in track_set:
      if (entryId not in tracks_in_playlist):
        print " Duplicate:: Title: %s (%s)" % (track['title'], track['artist'])
        total_delete += 1
        #api.delete_songs(entryId)
      else:
        print "  _In playlist:: Tile: %s (%s)" % (track['title'], track['artist'])
        total_skipped += 1
    else:
      track_set.add(calculated_string)
  print "====="
  print "Total Deleted: %d" % total_delete
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
  in_playlist = build_songs_in_playlists(api, all_playlists)
  print "Searching for duplicates."
  find_and_remove_dups(api, full_library, in_playlist)