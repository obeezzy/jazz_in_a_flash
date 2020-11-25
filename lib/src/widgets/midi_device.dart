import 'dart:core';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_midi_command/flutter_midi_command.dart' as fmc;
import 'package:google_fonts/google_fonts.dart';
import '../common/note.dart';

class MidiDevice {
  String id;
  fmc.MidiDevice _device;
  Function(Note note) onNotePressed;

  MidiDevice() {
    _init();
    _connect();
  }

  void _init() async {
    await for (String message in fmc.MidiCommand().onMidiSetupChanged) {
      switch (message) {
        case 'deviceFound':
          if (_device == null) await this._connect();
          break;
        case 'deviceLost':
          _device = null;
          break;
      }
    }

    await for (Uint8List midiData in fmc.MidiCommand().onMidiDataReceived) {
      final bool isNoteOnEvent = midiData.length > 3 && midiData[0] == 144;
      if (isNoteOnEvent) {
        final note = Note(midiData: midiData);
        this.onNotePressed(note);
        print('Note pressed: $note');
      }
    }
  }

  void _connect() async {
    if (id == null) {
      final List<fmc.MidiDevice> devices = await fmc.MidiCommand().devices;
      _device = devices.last;
      fmc.MidiCommand().connectToDevice(_device);
      print('Last found device=${devices.last.toDictionary}');
    }
  }
}
