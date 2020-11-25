import 'dart:core';
import 'dart:typed_data';

class Note {
  Uint8List _midiData;
  String _tone;
  DateTime timestamp;

  Note({Uint8List midiData, String tone}) {
    _midiData = midiData;
    _tone = tone;
    timestamp = DateTime.now();
  }

  String get pitch {
    return '';
  }

  String get tone {
    return '';
  }

  double get velocity {
    return 0;
  }

  @override
  String toString() => 'Note(pitch=$pitch, velocity=$velocity)';
}
