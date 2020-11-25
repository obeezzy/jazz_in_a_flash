import './note.dart';

class Chord {
  List<Note> notes;
  String name;
  String fullName;

  Chord({String name, List<Note> notes}) {}
}

class ChordDictionary {
  static List<Chord> get allChords {
    return [
      Chord(name: 'Cmaj7', notes: [
        Note(tone: 'C'),
        Note(tone: 'E'),
        Note(tone: 'G'),
        Note(tone: 'B')
      ])
    ];
  }
}
