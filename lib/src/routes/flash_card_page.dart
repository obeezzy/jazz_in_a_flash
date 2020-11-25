import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import '../common/random_chord_generator.dart';
import '../widgets/chord_detail_view.dart';
import '../widgets/chord_name_view.dart';
import '../widgets/midi_device.dart';

class FlashCardPage extends StatefulWidget {
  const FlashCardPage({Key key}) : super(key: key);

  @override
  _FlashCardPageState createState() => _FlashCardPageState();
}

class _FlashCardPageState extends State<FlashCardPage>
    with WidgetsBindingObserver {
  MidiDevice _midiDevice;
  RandomChordGenerator _chordGenerator;
  bool _revealed = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _midiDevice = MidiDevice();
    _chordGenerator = RandomChordGenerator();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    switch (state) {
      case AppLifecycleState.resumed:
        _midiDevice = MidiDevice();
        break;
      default:
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Jazz In A Flash'),
      ),
      body: GestureDetector(
        child: _revealed
            ? Center(
                child: ChordDetailView(),
              )
            : Center(
                child: ChordNameView(),
              ),
        onTap: () {
          setState(() => _revealed = !_revealed);
        },
      ),
    );
  }
}
