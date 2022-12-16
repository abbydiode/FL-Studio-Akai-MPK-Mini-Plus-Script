# name=Akai MPK Mini Plus
# url=https://github.com/abbydiode/fl-studio-akai-mpk-mini-plus-script
# supportedDevices=MPK mini Plus

import transport, general, mixer, midi

BUTTON_PREVIOUS = 0x73
BUTTON_NEXT = 0x74
BUTTON_STOP = 0x75
BUTTON_PLAY = 0x76
BUTTON_RECORD = 0x77

def OnControlChange(event):
    event.handled = False
    if event.data2 > 0:
        if event.data1 == BUTTON_PREVIOUS or event.data1 == BUTTON_NEXT:
            should_forward = event.data1 == BUTTON_NEXT
            numerator = general.getRecPPB() / general.getRecPPQ()
            ms_per_bar = 60000 / mixer.getCurrentTempo(1) * numerator
            new_song_pos = transport.getSongPos(midi.SONGLENGTH_MS) + (ms_per_bar if should_forward else -ms_per_bar)
            print(f'{"Forwarding" if should_forward else "Rewinding"} {round(new_song_pos / 1000)}/{transport.getSongLength(midi.SONGLENGTH_S)}s')
            transport.setSongPos(new_song_pos, midi.SONGLENGTH_MS)
        elif event.data1 == BUTTON_PLAY:
            print(f'{"Paused" if transport.isPlaying() else "Started"} playback')
            transport.start()
        elif event.data1 == BUTTON_STOP:
            print('Stopped playback')
            transport.stop()
        elif event.data1 == BUTTON_RECORD:
            print(f'{"Disabled" if transport.isRecording() else "Enabled"} recording')
            transport.record()
        event.handled = True